"""
Database Connection Pooling and Optimization
High-performance database operations with connection pooling, query optimization, and monitoring
"""
import os
import time
import threading
from typing import Dict, List, Any, Optional, Union, Tuple
from dataclasses import dataclass
from contextlib import contextmanager
from functools import wraps
import logging
from datetime import datetime, timedelta
import json

try:
    import psycopg2
    from psycopg2 import pool
    from psycopg2.extras import RealDictCursor, execute_values
    from psycopg2.extensions import ISOLATION_LEVEL_AUTOCOMMIT
    PSYCOPG2_AVAILABLE = True
except ImportError:
    PSYCOPG2_AVAILABLE = False
    psycopg2 = None
    pool = None
    RealDictCursor = None
    execute_values = None
    ISOLATION_LEVEL_AUTOCOMMIT = None

try:
    import redis
    from redis.connection import ConnectionPool
    REDIS_AVAILABLE = True
except ImportError:
    REDIS_AVAILABLE = False
    redis = None
    ConnectionPool = None

from utils.logger import get_logger, log_performance

logger = get_logger(__name__)

@dataclass
class DatabaseConfig:
    """Database configuration"""
    host: str
    port: int
    database: str
    username: str
    password: str
    min_connections: int = 5
    max_connections: int = 20
    connection_timeout: int = 30
    query_timeout: int = 60
    ssl_mode: str = 'prefer'
    application_name: str = 'marketing-agent'

@dataclass
class QueryMetrics:
    """Query performance metrics"""
    query: str
    execution_time_ms: float
    rows_affected: int
    connection_id: str
    timestamp: datetime

class DatabaseConnectionPool:
    """High-performance database connection pool"""
    
    def __init__(self, config: DatabaseConfig):
        self.config = config
        self.pool = None
        self.metrics: List[QueryMetrics] = []
        self.metrics_lock = threading.Lock()
        self._initialize_pool()
    
    def _initialize_pool(self):
        """Initialize connection pool"""
        if not PSYCOPG2_AVAILABLE:
            logger.warning("psycopg2 not available, database operations disabled")
            return
        
        try:
            # Create connection pool
            self.pool = psycopg2.pool.ThreadedConnectionPool(
                minconn=self.config.min_connections,
                maxconn=self.config.max_connections,
                host=self.config.host,
                port=self.config.port,
                database=self.config.database,
                user=self.config.username,
                password=self.config.password,
                connect_timeout=self.config.connection_timeout,
                application_name=self.config.application_name,
                sslmode=self.config.ssl_mode
            )
            logger.info(f"Database connection pool initialized: {self.config.min_connections}-{self.config.max_connections} connections")
        except Exception as e:
            logger.error(f"Failed to initialize database pool: {e}")
            raise
    
    @contextmanager
    def get_connection(self):
        """Get database connection from pool"""
        if not self.pool:
            raise RuntimeError("Database pool not initialized")
        
        connection = None
        start_time = time.time()
        
        try:
            connection = self.pool.getconn()
            if connection:
                connection.set_isolation_level(ISOLATION_LEVEL_AUTOCOMMIT)
            yield connection
        except Exception as e:
            if connection:
                connection.rollback()
            logger.error(f"Database connection error: {e}")
            raise
        finally:
            if connection:
                self.pool.putconn(connection)
                connection_time = (time.time() - start_time) * 1000
                logger.debug(f"Connection returned to pool in {connection_time:.2f}ms")
    
    def execute_query(self, query: str, params: Tuple = None, fetch: bool = True) -> List[Dict[str, Any]]:
        """Execute database query with performance monitoring"""
        start_time = time.time()
        connection_id = None
        
        try:
            with self.get_connection() as conn:
                if conn:
                    connection_id = str(id(conn))
                    cursor = conn.cursor(cursor_factory=RealDictCursor)
                    
                    try:
                        cursor.execute(query, params)
                        
                        if fetch:
                            results = cursor.fetchall()
                            rows_affected = len(results)
                        else:
                            rows_affected = cursor.rowcount
                            results = []
                        
                        # Record metrics
                        execution_time = (time.time() - start_time) * 1000
                        self._record_metrics(query, execution_time, rows_affected, connection_id)
                        
                        return results
                    finally:
                        cursor.close()
        except Exception as e:
            execution_time = (time.time() - start_time) * 1000
            logger.error(f"Query execution failed: {query[:100]}... Error: {e}")
            logger.error(f"Query execution time: {execution_time:.2f}ms")
            raise
    
    def execute_batch(self, query: str, params_list: List[Tuple]) -> int:
        """Execute batch operations efficiently"""
        start_time = time.time()
        connection_id = None
        
        try:
            with self.get_connection() as conn:
                if conn:
                    connection_id = str(id(conn))
                    cursor = conn.cursor()
                    
                    try:
                        execute_values(cursor, query, params_list)
                        rows_affected = cursor.rowcount
                        
                        # Record metrics
                        execution_time = (time.time() - start_time) * 1000
                        self._record_metrics(f"BATCH: {query}", execution_time, rows_affected, connection_id)
                        
                        return rows_affected
                    finally:
                        cursor.close()
        except Exception as e:
            execution_time = (time.time() - start_time) * 1000
            logger.error(f"Batch execution failed: {query[:100]}... Error: {e}")
            logger.error(f"Batch execution time: {execution_time:.2f}ms")
            raise
    
    def _record_metrics(self, query: str, execution_time_ms: float, rows_affected: int, connection_id: str):
        """Record query performance metrics"""
        with self.metrics_lock:
            metric = QueryMetrics(
                query=query[:200] + "..." if len(query) > 200 else query,
                execution_time_ms=execution_time_ms,
                rows_affected=rows_affected,
                connection_id=connection_id,
                timestamp=datetime.now()
            )
            self.metrics.append(metric)
            
            # Keep only last 1000 metrics
            if len(self.metrics) > 1000:
                self.metrics = self.metrics[-1000:]
    
    def get_performance_stats(self, hours: int = 1) -> Dict[str, Any]:
        """Get database performance statistics"""
        with self.metrics_lock:
            cutoff_time = datetime.now() - timedelta(hours=hours)
            recent_metrics = [m for m in self.metrics if m.timestamp > cutoff_time]
        
        if not recent_metrics:
            return {}
        
        execution_times = [m.execution_time_ms for m in recent_metrics]
        rows_affected = [m.rows_affected for m in recent_metrics]
        
        return {
            'total_queries': len(recent_metrics),
            'avg_execution_time_ms': sum(execution_times) / len(execution_times),
            'min_execution_time_ms': min(execution_times),
            'max_execution_time_ms': max(execution_times),
            'total_rows_affected': sum(rows_affected),
            'slow_queries': len([t for t in execution_times if t > 1000]),  # > 1 second
            'pool_size': self.pool.maxconn if self.pool else 0,
            'active_connections': self.pool.maxconn - self.pool.minconn if self.pool else 0
        }
    
    def close_pool(self):
        """Close connection pool"""
        if self.pool:
            self.pool.closeall()
            logger.info("Database connection pool closed")

class RedisCache:
    """High-performance Redis caching layer"""
    
    def __init__(self, host: str = 'localhost', port: int = 6379, 
                 password: str = None, db: int = 0, max_connections: int = 20):
        self.config = {
            'host': host,
            'port': port,
            'password': password,
            'db': db,
            'max_connections': max_connections
        }
        self.pool = None
        self.redis_client = None
        self._initialize_redis()
    
    def _initialize_redis(self):
        """Initialize Redis connection pool"""
        if not REDIS_AVAILABLE:
            logger.warning("Redis not available, caching disabled")
            return
        
        try:
            # Create connection pool
            self.pool = ConnectionPool(
                host=self.config['host'],
                port=self.config['port'],
                password=self.config['password'],
                db=self.config['db'],
                max_connections=self.config['max_connections']
            )
            
            self.redis_client = redis.Redis(connection_pool=self.pool)
            
            # Test connection
            self.redis_client.ping()
            logger.info(f"Redis connection pool initialized: {self.config['max_connections']} connections")
        except Exception as e:
            logger.error(f"Failed to initialize Redis: {e}")
            self.redis_client = None
    
    def get(self, key: str) -> Optional[Any]:
        """Get value from cache"""
        if not self.redis_client:
            return None
        
        try:
            value = self.redis_client.get(key)
            if value:
                return json.loads(value)
            return None
        except Exception as e:
            logger.error(f"Redis get error for key {key}: {e}")
            return None
    
    def set(self, key: str, value: Any, ttl: int = 3600) -> bool:
        """Set value in cache with TTL"""
        if not self.redis_client:
            return False
        
        try:
            serialized_value = json.dumps(value, default=str)
            return self.redis_client.setex(key, ttl, serialized_value)
        except Exception as e:
            logger.error(f"Redis set error for key {key}: {e}")
            return False
    
    def delete(self, key: str) -> bool:
        """Delete key from cache"""
        if not self.redis_client:
            return False
        
        try:
            return bool(self.redis_client.delete(key))
        except Exception as e:
            logger.error(f"Redis delete error for key {key}: {e}")
            return False
    
    def exists(self, key: str) -> bool:
        """Check if key exists in cache"""
        if not self.redis_client:
            return False
        
        try:
            return bool(self.redis_client.exists(key))
        except Exception as e:
            logger.error(f"Redis exists error for key {key}: {e}")
            return False
    
    def get_stats(self) -> Dict[str, Any]:
        """Get Redis statistics"""
        if not self.redis_client:
            return {}
        
        try:
            info = self.redis_client.info()
            return {
                'connected_clients': info.get('connected_clients', 0),
                'used_memory': info.get('used_memory', 0),
                'used_memory_human': info.get('used_memory_human', '0B'),
                'keyspace_hits': info.get('keyspace_hits', 0),
                'keyspace_misses': info.get('keyspace_misses', 0),
                'hit_rate': info.get('keyspace_hits', 0) / (info.get('keyspace_hits', 0) + info.get('keyspace_misses', 1)) * 100
            }
        except Exception as e:
            logger.error(f"Redis stats error: {e}")
            return {}

class DatabaseManager:
    """Centralized database management"""
    
    def __init__(self):
        self.db_pool = None
        self.redis_cache = None
        self._initialize_databases()
    
    def _initialize_databases(self):
        """Initialize database connections"""
        # PostgreSQL configuration
        db_config = DatabaseConfig(
            host=os.getenv('POSTGRES_HOST', 'localhost'),
            port=int(os.getenv('POSTGRES_PORT', '5432')),
            database=os.getenv('POSTGRES_DB', 'marketing_agent'),
            username=os.getenv('POSTGRES_USER', 'marketing_agent'),
            password=os.getenv('POSTGRES_PASSWORD', ''),
            min_connections=int(os.getenv('DB_MIN_CONNECTIONS', '5')),
            max_connections=int(os.getenv('DB_MAX_CONNECTIONS', '20')),
            connection_timeout=int(os.getenv('DB_CONNECTION_TIMEOUT', '30')),
            query_timeout=int(os.getenv('DB_QUERY_TIMEOUT', '60'))
        )
        
        try:
            self.db_pool = DatabaseConnectionPool(db_config)
            logger.info("Database manager initialized successfully")
        except Exception as e:
            logger.error(f"Failed to initialize database manager: {e}")
        
        # Redis configuration
        redis_config = {
            'host': os.getenv('REDIS_HOST', 'localhost'),
            'port': int(os.getenv('REDIS_PORT', '6379')),
            'password': os.getenv('REDIS_PASSWORD'),
            'db': int(os.getenv('REDIS_DB', '0')),
            'max_connections': int(os.getenv('REDIS_MAX_CONNECTIONS', '20'))
        }
        
        try:
            self.redis_cache = RedisCache(**redis_config)
            logger.info("Redis cache initialized successfully")
        except Exception as e:
            logger.error(f"Failed to initialize Redis cache: {e}")
    
    def execute_query(self, query: str, params: Tuple = None, use_cache: bool = False, 
                     cache_key: str = None, cache_ttl: int = 3600) -> List[Dict[str, Any]]:
        """Execute query with optional caching"""
        # Check cache first
        if use_cache and cache_key and self.redis_cache:
            cached_result = self.redis_cache.get(cache_key)
            if cached_result is not None:
                logger.debug(f"Cache hit for key: {cache_key}")
                return cached_result
        
        # Execute query
        if not self.db_pool:
            raise RuntimeError("Database pool not initialized")
        
        result = self.db_pool.execute_query(query, params)
        
        # Cache result
        if use_cache and cache_key and self.redis_cache:
            self.redis_cache.set(cache_key, result, cache_ttl)
            logger.debug(f"Cached result for key: {cache_key}")
        
        return result
    
    def get_performance_stats(self) -> Dict[str, Any]:
        """Get database performance statistics"""
        stats = {}
        
        if self.db_pool:
            stats['database'] = self.db_pool.get_performance_stats()
        
        if self.redis_cache:
            stats['redis'] = self.redis_cache.get_stats()
        
        return stats
    
    def close_connections(self):
        """Close all database connections"""
        if self.db_pool:
            self.db_pool.close_pool()
        
        if self.redis_cache and self.redis_cache.redis_client:
            self.redis_cache.redis_client.close()

# Global database manager instance
db_manager = DatabaseManager()

def get_database_manager() -> DatabaseManager:
    """Get database manager instance"""
    return db_manager

def cache_result(cache_key: str, ttl: int = 3600):
    """Decorator to cache function results"""
    def decorator(func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            # Generate cache key
            key = f"{cache_key}:{hash(str(args) + str(kwargs))}"
            
            # Check cache
            if db_manager.redis_cache:
                cached_result = db_manager.redis_cache.get(key)
                if cached_result is not None:
                    logger.debug(f"Cache hit for function {func.__name__}")
                    return cached_result
            
            # Execute function
            result = func(*args, **kwargs)
            
            # Cache result
            if db_manager.redis_cache:
                db_manager.redis_cache.set(key, result, ttl)
                logger.debug(f"Cached result for function {func.__name__}")
            
            return result
        return wrapper
    return decorator

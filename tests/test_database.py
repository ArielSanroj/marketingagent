"""
Comprehensive tests for the database system
"""
import pytest
import os
import tempfile
from unittest.mock import patch, MagicMock, Mock
from datetime import datetime

from utils.database import (
    DatabaseConfig, DatabaseConnectionPool, RedisCache, DatabaseManager,
    get_database_manager, cache_result, QueryMetrics
)

class TestDatabaseConfig:
    """Test DatabaseConfig functionality"""
    
    def test_database_config_initialization(self):
        """Test database config initialization"""
        config = DatabaseConfig(
            host="localhost",
            port=5432,
            database="test_db",
            username="test_user",
            password="test_password"
        )
        
        assert config.host == "localhost"
        assert config.port == 5432
        assert config.database == "test_db"
        assert config.username == "test_user"
        assert config.password == "test_password"
        assert config.min_connections == 5
        assert config.max_connections == 20
    
    def test_database_config_with_custom_values(self):
        """Test database config with custom values"""
        config = DatabaseConfig(
            host="custom_host",
            port=3306,
            database="custom_db",
            username="custom_user",
            password="custom_password",
            min_connections=10,
            max_connections=50,
            connection_timeout=60,
            query_timeout=120,
            ssl_mode="require",
            application_name="custom_app"
        )
        
        assert config.host == "custom_host"
        assert config.port == 3306
        assert config.min_connections == 10
        assert config.max_connections == 50
        assert config.connection_timeout == 60
        assert config.query_timeout == 120
        assert config.ssl_mode == "require"
        assert config.application_name == "custom_app"

class TestQueryMetrics:
    """Test QueryMetrics functionality"""
    
    def test_query_metrics_initialization(self):
        """Test query metrics initialization"""
        metrics = QueryMetrics(
            query="SELECT * FROM test_table",
            execution_time_ms=150.5,
            rows_affected=10,
            connection_id="conn_123",
            timestamp=datetime.now()
        )
        
        assert metrics.query == "SELECT * FROM test_table"
        assert metrics.execution_time_ms == 150.5
        assert metrics.rows_affected == 10
        assert metrics.connection_id == "conn_123"
        assert isinstance(metrics.timestamp, datetime)

@patch('utils.database.psycopg2')
class TestDatabaseConnectionPool:
    """Test DatabaseConnectionPool functionality"""
    
    def test_connection_pool_initialization(self, mock_psycopg2):
        """Test connection pool initialization"""
        mock_pool = MagicMock()
        mock_psycopg2.pool.ThreadedConnectionPool.return_value = mock_pool
        
        config = DatabaseConfig(
            host="localhost",
            port=5432,
            database="test_db",
            username="test_user",
            password="test_password"
        )
        
        pool = DatabaseConnectionPool(config)
        
        assert pool.config == config
        assert pool.pool == mock_pool
        mock_psycopg2.pool.ThreadedConnectionPool.assert_called_once()
    
    def test_connection_pool_without_psycopg2(self, mock_psycopg2):
        """Test connection pool without psycopg2"""
        mock_psycopg2.side_effect = ImportError("psycopg2 not available")
        
        config = DatabaseConfig(
            host="localhost",
            port=5432,
            database="test_db",
            username="test_user",
            password="test_password"
        )
        
        pool = DatabaseConnectionPool(config)
        assert pool.pool is None
    
    def test_get_connection_success(self, mock_psycopg2):
        """Test successful connection retrieval"""
        mock_pool = MagicMock()
        mock_connection = MagicMock()
        mock_pool.getconn.return_value = mock_connection
        mock_psycopg2.pool.ThreadedConnectionPool.return_value = mock_pool
        
        config = DatabaseConfig(
            host="localhost",
            port=5432,
            database="test_db",
            username="test_user",
            password="test_password"
        )
        
        pool = DatabaseConnectionPool(config)
        
        with pool.get_connection() as conn:
            assert conn == mock_connection
            mock_pool.getconn.assert_called_once()
            mock_pool.putconn.assert_called_once_with(mock_connection)
    
    def test_get_connection_failure(self, mock_psycopg2):
        """Test connection retrieval failure"""
        mock_pool = MagicMock()
        mock_pool.getconn.side_effect = Exception("Connection failed")
        mock_psycopg2.pool.ThreadedConnectionPool.return_value = mock_pool
        
        config = DatabaseConfig(
            host="localhost",
            port=5432,
            database="test_db",
            username="test_user",
            password="test_password"
        )
        
        pool = DatabaseConnectionPool(config)
        
        with pytest.raises(Exception, match="Connection failed"):
            with pool.get_connection() as conn:
                pass
    
    def test_execute_query_success(self, mock_psycopg2):
        """Test successful query execution"""
        mock_pool = MagicMock()
        mock_connection = MagicMock()
        mock_cursor = MagicMock()
        mock_cursor.fetchall.return_value = [{'id': 1, 'name': 'test'}]
        mock_connection.cursor.return_value = mock_cursor
        mock_pool.getconn.return_value = mock_connection
        mock_psycopg2.pool.ThreadedConnectionPool.return_value = mock_pool
        mock_psycopg2.extras.RealDictCursor = MagicMock()
        
        config = DatabaseConfig(
            host="localhost",
            port=5432,
            database="test_db",
            username="test_user",
            password="test_password"
        )
        
        pool = DatabaseConnectionPool(config)
        
        result = pool.execute_query("SELECT * FROM test_table")
        
        assert result == [{'id': 1, 'name': 'test'}]
        mock_cursor.execute.assert_called_once_with("SELECT * FROM test_table", None)
        mock_cursor.fetchall.assert_called_once()
        mock_cursor.close.assert_called_once()
    
    def test_execute_query_failure(self, mock_psycopg2):
        """Test query execution failure"""
        mock_pool = MagicMock()
        mock_connection = MagicMock()
        mock_cursor = MagicMock()
        mock_cursor.execute.side_effect = Exception("Query failed")
        mock_connection.cursor.return_value = mock_cursor
        mock_pool.getconn.return_value = mock_connection
        mock_psycopg2.pool.ThreadedConnectionPool.return_value = mock_pool
        mock_psycopg2.extras.RealDictCursor = MagicMock()
        
        config = DatabaseConfig(
            host="localhost",
            port=5432,
            database="test_db",
            username="test_user",
            password="test_password"
        )
        
        pool = DatabaseConnectionPool(config)
        
        with pytest.raises(Exception, match="Query failed"):
            pool.execute_query("SELECT * FROM test_table")
    
    def test_execute_batch_success(self, mock_psycopg2):
        """Test successful batch execution"""
        mock_pool = MagicMock()
        mock_connection = MagicMock()
        mock_cursor = MagicMock()
        mock_cursor.rowcount = 5
        mock_connection.cursor.return_value = mock_cursor
        mock_pool.getconn.return_value = mock_connection
        mock_psycopg2.pool.ThreadedConnectionPool.return_value = mock_pool
        mock_psycopg2.extras.execute_values = MagicMock()
        
        config = DatabaseConfig(
            host="localhost",
            port=5432,
            database="test_db",
            username="test_user",
            password="test_password"
        )
        
        pool = DatabaseConnectionPool(config)
        
        params_list = [('value1',), ('value2',)]
        result = pool.execute_batch("INSERT INTO test_table VALUES %s", params_list)
        
        assert result == 5
        mock_psycopg2.extras.execute_values.assert_called_once()
        mock_cursor.close.assert_called_once()
    
    def test_get_performance_stats(self, mock_psycopg2):
        """Test getting performance statistics"""
        mock_pool = MagicMock()
        mock_pool.maxconn = 20
        mock_pool.minconn = 5
        mock_psycopg2.pool.ThreadedConnectionPool.return_value = mock_pool
        
        config = DatabaseConfig(
            host="localhost",
            port=5432,
            database="test_db",
            username="test_user",
            password="test_password"
        )
        
        pool = DatabaseConnectionPool(config)
        
        # Add some mock metrics
        pool.metrics = [
            QueryMetrics(
                query="SELECT * FROM test",
                execution_time_ms=100.0,
                rows_affected=5,
                connection_id="conn1",
                timestamp=datetime.now()
            ),
            QueryMetrics(
                query="SELECT * FROM test2",
                execution_time_ms=200.0,
                rows_affected=10,
                connection_id="conn2",
                timestamp=datetime.now()
            )
        ]
        
        stats = pool.get_performance_stats()
        
        assert stats['total_queries'] == 2
        assert stats['avg_execution_time_ms'] == 150.0
        assert stats['min_execution_time_ms'] == 100.0
        assert stats['max_execution_time_ms'] == 200.0
        assert stats['total_rows_affected'] == 15
        assert stats['pool_size'] == 20
    
    def test_close_pool(self, mock_psycopg2):
        """Test closing connection pool"""
        mock_pool = MagicMock()
        mock_psycopg2.pool.ThreadedConnectionPool.return_value = mock_pool
        
        config = DatabaseConfig(
            host="localhost",
            port=5432,
            database="test_db",
            username="test_user",
            password="test_password"
        )
        
        pool = DatabaseConnectionPool(config)
        pool.close_pool()
        
        mock_pool.closeall.assert_called_once()

@patch('utils.database.redis')
class TestRedisCache:
    """Test RedisCache functionality"""
    
    def test_redis_cache_initialization(self, mock_redis):
        """Test Redis cache initialization"""
        mock_redis.Redis.return_value.ping.return_value = True
        
        cache = RedisCache(
            host="localhost",
            port=6379,
            password="test_password",
            db=0,
            max_connections=20
        )
        
        assert cache.config['host'] == "localhost"
        assert cache.config['port'] == 6379
        assert cache.config['password'] == "test_password"
        assert cache.config['db'] == 0
        assert cache.config['max_connections'] == 20
        assert cache.redis_client is not None
    
    def test_redis_cache_without_redis(self, mock_redis):
        """Test Redis cache without redis library"""
        mock_redis.side_effect = ImportError("redis not available")
        
        cache = RedisCache()
        
        assert cache.redis_client is None
    
    def test_redis_cache_connection_failure(self, mock_redis):
        """Test Redis cache connection failure"""
        mock_redis.Redis.return_value.ping.side_effect = Exception("Connection failed")
        
        cache = RedisCache()
        
        assert cache.redis_client is None
    
    def test_get_success(self, mock_redis):
        """Test successful get operation"""
        mock_client = MagicMock()
        mock_client.get.return_value = '{"key": "value"}'
        mock_redis.Redis.return_value = mock_client
        mock_redis.Redis.return_value.ping.return_value = True
        
        cache = RedisCache()
        
        result = cache.get("test_key")
        
        assert result == {"key": "value"}
        mock_client.get.assert_called_once_with("test_key")
    
    def test_get_not_found(self, mock_redis):
        """Test get operation when key not found"""
        mock_client = MagicMock()
        mock_client.get.return_value = None
        mock_redis.Redis.return_value = mock_client
        mock_redis.Redis.return_value.ping.return_value = True
        
        cache = RedisCache()
        
        result = cache.get("test_key")
        
        assert result is None
    
    def test_get_error(self, mock_redis):
        """Test get operation with error"""
        mock_client = MagicMock()
        mock_client.get.side_effect = Exception("Redis error")
        mock_redis.Redis.return_value = mock_client
        mock_redis.Redis.return_value.ping.return_value = True
        
        cache = RedisCache()
        
        result = cache.get("test_key")
        
        assert result is None
    
    def test_set_success(self, mock_redis):
        """Test successful set operation"""
        mock_client = MagicMock()
        mock_client.setex.return_value = True
        mock_redis.Redis.return_value = mock_client
        mock_redis.Redis.return_value.ping.return_value = True
        
        cache = RedisCache()
        
        result = cache.set("test_key", {"key": "value"}, 3600)
        
        assert result is True
        mock_client.setex.assert_called_once()
    
    def test_set_error(self, mock_redis):
        """Test set operation with error"""
        mock_client = MagicMock()
        mock_client.setex.side_effect = Exception("Redis error")
        mock_redis.Redis.return_value = mock_client
        mock_redis.Redis.return_value.ping.return_value = True
        
        cache = RedisCache()
        
        result = cache.set("test_key", {"key": "value"}, 3600)
        
        assert result is False
    
    def test_delete_success(self, mock_redis):
        """Test successful delete operation"""
        mock_client = MagicMock()
        mock_client.delete.return_value = 1
        mock_redis.Redis.return_value = mock_client
        mock_redis.Redis.return_value.ping.return_value = True
        
        cache = RedisCache()
        
        result = cache.delete("test_key")
        
        assert result is True
        mock_client.delete.assert_called_once_with("test_key")
    
    def test_exists_success(self, mock_redis):
        """Test successful exists operation"""
        mock_client = MagicMock()
        mock_client.exists.return_value = 1
        mock_redis.Redis.return_value = mock_client
        mock_redis.Redis.return_value.ping.return_value = True
        
        cache = RedisCache()
        
        result = cache.exists("test_key")
        
        assert result is True
        mock_client.exists.assert_called_once_with("test_key")
    
    def test_get_stats_success(self, mock_redis):
        """Test successful get stats operation"""
        mock_client = MagicMock()
        mock_client.info.return_value = {
            'connected_clients': 5,
            'used_memory': 1024000,
            'used_memory_human': '1MB',
            'keyspace_hits': 100,
            'keyspace_misses': 10
        }
        mock_redis.Redis.return_value = mock_client
        mock_redis.Redis.return_value.ping.return_value = True
        
        cache = RedisCache()
        
        stats = cache.get_stats()
        
        assert stats['connected_clients'] == 5
        assert stats['used_memory'] == 1024000
        assert stats['hit_rate'] == 100 / 110 * 100
    
    def test_get_stats_error(self, mock_redis):
        """Test get stats operation with error"""
        mock_client = MagicMock()
        mock_client.info.side_effect = Exception("Redis error")
        mock_redis.Redis.return_value = mock_client
        mock_redis.Redis.return_value.ping.return_value = True
        
        cache = RedisCache()
        
        stats = cache.get_stats()
        
        assert stats == {}

class TestDatabaseManager:
    """Test DatabaseManager functionality"""
    
    @patch('utils.database.DatabaseConnectionPool')
    @patch('utils.database.RedisCache')
    def test_database_manager_initialization(self, mock_redis_cache, mock_db_pool):
        """Test database manager initialization"""
        mock_db_pool.return_value = MagicMock()
        mock_redis_cache.return_value = MagicMock()
        
        manager = DatabaseManager()
        
        assert manager.db_pool is not None
        assert manager.redis_cache is not None
    
    @patch('utils.database.DatabaseConnectionPool')
    @patch('utils.database.RedisCache')
    def test_execute_query_with_cache(self, mock_redis_cache, mock_db_pool):
        """Test execute query with caching"""
        mock_db_pool.return_value = MagicMock()
        mock_redis_cache.return_value = MagicMock()
        mock_redis_cache.return_value.get.return_value = {"cached": "data"}
        
        manager = DatabaseManager()
        
        result = manager.execute_query(
            "SELECT * FROM test",
            use_cache=True,
            cache_key="test_key"
        )
        
        assert result == {"cached": "data"}
        mock_redis_cache.return_value.get.assert_called_once_with("test_key")
    
    @patch('utils.database.DatabaseConnectionPool')
    @patch('utils.database.RedisCache')
    def test_execute_query_without_cache(self, mock_redis_cache, mock_db_pool):
        """Test execute query without caching"""
        mock_db_pool.return_value = MagicMock()
        mock_db_pool.return_value.execute_query.return_value = [{"result": "data"}]
        mock_redis_cache.return_value = MagicMock()
        mock_redis_cache.return_value.get.return_value = None
        
        manager = DatabaseManager()
        
        result = manager.execute_query("SELECT * FROM test")
        
        assert result == [{"result": "data"}]
        mock_db_pool.return_value.execute_query.assert_called_once_with("SELECT * FROM test", None)
    
    @patch('utils.database.DatabaseConnectionPool')
    @patch('utils.database.RedisCache')
    def test_get_performance_stats(self, mock_redis_cache, mock_db_pool):
        """Test getting performance statistics"""
        mock_db_pool.return_value = MagicMock()
        mock_db_pool.return_value.get_performance_stats.return_value = {"db_stats": "data"}
        mock_redis_cache.return_value = MagicMock()
        mock_redis_cache.return_value.get_stats.return_value = {"redis_stats": "data"}
        
        manager = DatabaseManager()
        
        stats = manager.get_performance_stats()
        
        assert stats['database'] == {"db_stats": "data"}
        assert stats['redis'] == {"redis_stats": "data"}
    
    @patch('utils.database.DatabaseConnectionPool')
    @patch('utils.database.RedisCache')
    def test_close_connections(self, mock_redis_cache, mock_db_pool):
        """Test closing connections"""
        mock_db_pool.return_value = MagicMock()
        mock_redis_cache.return_value = MagicMock()
        mock_redis_cache.return_value.redis_client = MagicMock()
        
        manager = DatabaseManager()
        manager.close_connections()
        
        mock_db_pool.return_value.close_pool.assert_called_once()
        mock_redis_cache.return_value.redis_client.close.assert_called_once()

class TestCacheResultDecorator:
    """Test cache_result decorator"""
    
    @patch('utils.database.get_database_manager')
    def test_cache_result_decorator(self, mock_get_db_manager):
        """Test cache_result decorator functionality"""
        mock_db_manager = MagicMock()
        mock_db_manager.redis_cache = MagicMock()
        mock_db_manager.redis_cache.get.return_value = None
        mock_db_manager.redis_cache.set.return_value = True
        mock_get_db_manager.return_value = mock_db_manager
        
        @cache_result("test_cache_key", ttl=3600)
        def test_function():
            return "test_result"
        
        result = test_function()
        
        assert result == "test_result"
        mock_db_manager.redis_cache.get.assert_called_once()
        mock_db_manager.redis_cache.set.assert_called_once()
    
    @patch('utils.database.get_database_manager')
    def test_cache_result_decorator_with_cache_hit(self, mock_get_db_manager):
        """Test cache_result decorator with cache hit"""
        mock_db_manager = MagicMock()
        mock_db_manager.redis_cache = MagicMock()
        mock_db_manager.redis_cache.get.return_value = "cached_result"
        mock_get_db_manager.return_value = mock_db_manager
        
        @cache_result("test_cache_key", ttl=3600)
        def test_function():
            return "test_result"
        
        result = test_function()
        
        assert result == "cached_result"
        mock_db_manager.redis_cache.get.assert_called_once()
        mock_db_manager.redis_cache.set.assert_not_called()
    
    @patch('utils.database.get_database_manager')
    def test_cache_result_decorator_without_redis(self, mock_get_db_manager):
        """Test cache_result decorator without Redis"""
        mock_db_manager = MagicMock()
        mock_db_manager.redis_cache = None
        mock_get_db_manager.return_value = mock_db_manager
        
        @cache_result("test_cache_key", ttl=3600)
        def test_function():
            return "test_result"
        
        result = test_function()
        
        assert result == "test_result"

class TestGlobalFunctions:
    """Test global database functions"""
    
    @patch('utils.database.DatabaseManager')
    def test_get_database_manager(self, mock_db_manager):
        """Test get_database_manager function"""
        mock_instance = MagicMock()
        mock_db_manager.return_value = mock_instance
        
        from utils.database import get_database_manager
        
        result = get_database_manager()
        
        assert result == mock_instance


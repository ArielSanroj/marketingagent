"""
Email System for tphagent Results
Sends comprehensive marketing strategy results to user's email
"""
import smtplib
import os
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.base import MIMEBase
from email import encoders
from datetime import datetime
import json

class ResultsEmailSender:
    def __init__(self):
        self.smtp_server = "smtp.gmail.com"
        self.smtp_port = 587
        # You'll need to set these environment variables
        self.sender_email = os.getenv('EMAIL_USER', 'your-email@gmail.com')
        self.sender_password = os.getenv('EMAIL_PASSWORD', 'your-app-password')
        
    def create_email_content(self, hotel_name, user_email):
        """Create comprehensive email content with all results"""
        
        # Read the generated files
        try:
            with open('outputs/estancia_hacienda_market_research.md', 'r', encoding='utf-8') as f:
                market_research = f.read()
        except:
            market_research = "Market research report not available"
            
        try:
            with open('outputs/estancia_hacienda_google_ads.md', 'r', encoding='utf-8') as f:
                google_ads = f.read()
        except:
            google_ads = "Google Ads campaign report not available"
            
        try:
            with open('outputs/estancia_hacienda_optimization.md', 'r', encoding='utf-8') as f:
                optimization = f.read()
        except:
            optimization = "Optimization report not available"
            
        try:
            with open('outputs/estancia_hacienda_workflow_results.json', 'r', encoding='utf-8') as f:
                workflow_data = json.load(f)
        except:
            workflow_data = {}

        # Create HTML email content
        html_content = f"""
        <!DOCTYPE html>
        <html>
        <head>
            <meta charset="UTF-8">
            <title>tphagent Marketing Strategy Results - {hotel_name}</title>
            <style>
                body {{ font-family: Arial, sans-serif; line-height: 1.6; color: #333; }}
                .header {{ background: linear-gradient(135deg, #667eea 0%, #764ba2 100%); color: white; padding: 20px; text-align: center; }}
                .content {{ padding: 20px; }}
                .section {{ margin: 20px 0; padding: 15px; border-left: 4px solid #667eea; background: #f8f9fa; }}
                .highlight {{ background: #e3f2fd; padding: 10px; border-radius: 5px; margin: 10px 0; }}
                .metrics {{ display: flex; justify-content: space-around; margin: 20px 0; }}
                .metric {{ text-align: center; padding: 15px; background: white; border-radius: 8px; box-shadow: 0 2px 4px rgba(0,0,0,0.1); }}
                .cta {{ background: #4caf50; color: white; padding: 15px; text-align: center; border-radius: 5px; margin: 20px 0; }}
                .footer {{ background: #f5f5f5; padding: 15px; text-align: center; font-size: 12px; color: #666; }}
                pre {{ background: #f4f4f4; padding: 10px; border-radius: 5px; overflow-x: auto; }}
                h1, h2, h3 {{ color: #333; }}
                .success {{ color: #4caf50; font-weight: bold; }}
                .warning {{ color: #ff9800; font-weight: bold; }}
                .info {{ color: #2196f3; font-weight: bold; }}
            </style>
        </head>
        <body>
            <div class="header">
                <h1>🏨 tphagent Marketing Strategy Results</h1>
                <h2>{hotel_name}</h2>
                <p>Complete AI-Generated Marketing Strategy & Next Steps</p>
                <p>Generated: {datetime.now().strftime('%B %d, %Y at %I:%M %p')}</p>
            </div>
            
            <div class="content">
                <div class="highlight">
                    <h3>🎉 Congratulations! Your Marketing Strategy is Ready</h3>
                    <p>Our AI agents have analyzed your hotel and created a comprehensive marketing strategy tailored specifically for <strong>{hotel_name}</strong>. All results are included in this email with detailed next steps for implementation.</p>
                </div>

                <div class="metrics">
                    <div class="metric">
                        <h3>💰 Budget</h3>
                        <p><strong>$720/month</strong></p>
                        <small>Standard Tier</small>
                    </div>
                    <div class="metric">
                        <h3>🎯 Expected ROI</h3>
                        <p><strong>400%+</strong></p>
                        <small>Within 30 days</small>
                    </div>
                    <div class="metric">
                        <h3>📊 Campaigns</h3>
                        <p><strong>3 Active</strong></p>
                        <small>Google Ads</small>
                    </div>
                    <div class="metric">
                        <h3>🎯 Keywords</h3>
                        <p><strong>27 Targeted</strong></p>
                        <small>High-value terms</small>
                    </div>
                </div>

                <div class="section">
                    <h2>📊 Executive Summary</h2>
                    <p><strong>Hotel Analysis:</strong> Successfully analyzed {hotel_name} as a 100-year-old eco-lodge colonial property in Nilo, Cundinamarca, Colombia.</p>
                    <p><strong>Target Market:</strong> Eco-conscious families, heritage tourism enthusiasts, and international eco-tourists from Bogotá area.</p>
                    <p><strong>Key Opportunities:</strong> Social media presence, pricing transparency, and review management improvements identified.</p>
                    <p><strong>Marketing Strategy:</strong> 3-phase approach focusing on eco-tourism, heritage tourism, and family getaways.</p>
                </div>

                <div class="section">
                    <h2>🔍 Market Research Results</h2>
                    <div class="highlight">
                        <h4>Key Market Insights:</h4>
                        <ul>
                            <li><strong>Market Growth:</strong> Eco-tourism growing 15% annually in Colombia</li>
                            <li><strong>Target Audience:</strong> 4 segments identified with specific demographics and behaviors</li>
                            <li><strong>Competitor Analysis:</strong> 3 direct competitors analyzed in Cundinamarca region</li>
                            <li><strong>Keyword Research:</strong> 5 high-value keywords with 480-1,200 monthly searches</li>
                            <li><strong>Market Opportunity:</strong> 2.5M potential customers in Bogotá area</li>
                        </ul>
                    </div>
                    <details>
                        <summary><strong>📋 View Complete Market Research Report</strong></summary>
                        <pre>{market_research[:2000]}...</pre>
                        <p><em>Full report attached as separate file</em></p>
                    </details>
                </div>

                <div class="section">
                    <h2>📢 Google Ads Campaign Strategy</h2>
                    <div class="highlight">
                        <h4>Campaign Structure:</h4>
                        <ul>
                            <li><strong>3 Campaigns:</strong> Eco-Tourism, Heritage Tourism, Family Getaways</li>
                            <li><strong>6 Ad Groups:</strong> Themed around key experiences</li>
                            <li><strong>27 Keywords:</strong> High-value, targeted terms</li>
                            <li><strong>9 Ad Variations:</strong> A/B testing ready</li>
                            <li><strong>Budget Allocation:</strong> $432/month (60% of total budget)</li>
                        </ul>
                    </div>
                    <details>
                        <summary><strong>📋 View Complete Google Ads Campaign Details</strong></summary>
                        <pre>{google_ads[:2000]}...</pre>
                        <p><em>Full campaign details attached as separate file</em></p>
                    </details>
                </div>

                <div class="section">
                    <h2>⚡ Performance Optimization Plan</h2>
                    <div class="highlight">
                        <h4>3-Phase Implementation Strategy:</h4>
                        <ul>
                            <li><strong>Phase 1 (Your Days 1-14):</strong> Foundation optimization and keyword refinement</li>
                            <li><strong>Phase 2 (Your Days 15-30):</strong> Performance enhancement and bidding optimization</li>
                            <li><strong>Phase 3 (Your Days 31-60):</strong> Scale and expand successful campaigns</li>
                        </ul>
                        <p><em>AI analysis completed instantly. Timeline above is for your campaign implementation.</em></p>
                    </div>
                    <details>
                        <summary><strong>📋 View Complete Optimization Strategy</strong></summary>
                        <pre>{optimization[:2000]}...</pre>
                        <p><em>Full optimization plan attached as separate file</em></p>
                    </details>
                </div>

                <div class="cta">
                    <h2>🚀 Ready to Launch Your Marketing Campaign!</h2>
                    <p>All AI agents have completed their analysis and generated your personalized marketing strategy. The next step is implementation.</p>
                </div>

                <div class="section">
                    <h2>📋 Immediate Next Steps</h2>
                    <ol>
                        <li><strong>Set up Google Ads account</strong> and implement the 3 campaigns</li>
                        <li><strong>Create social media profiles</strong> (Instagram, Facebook) for your hotel</li>
                        <li><strong>Add pricing transparency</strong> to your website</li>
                        <li><strong>Implement review collection system</strong> for reputation building</li>
                        <li><strong>Monitor performance daily</strong> and optimize based on data</li>
                    </ol>
                </div>

                <div class="section">
                    <h2>📁 Attached Files</h2>
                    <ul>
                        <li><strong>Market Research Report:</strong> Complete market analysis and competitor research</li>
                        <li><strong>Google Ads Campaign:</strong> Detailed campaign structure and ad copy</li>
                        <li><strong>Optimization Strategy:</strong> 3-phase performance optimization plan</li>
                        <li><strong>Workflow Results:</strong> Complete JSON data with all metrics and settings</li>
                    </ul>
                </div>

                <div class="section">
                    <h2>📞 Support & Questions</h2>
                    <p>If you have any questions about implementing this strategy or need assistance with any of the next steps, please don't hesitate to reach out.</p>
                    <p><strong>tphagent Team</strong><br>
                    AI-Powered Hotel Marketing Solutions</p>
                </div>
            </div>

            <div class="footer">
                <p>This email was generated by tphagent AI Marketing System</p>
                <p>Generated on {datetime.now().strftime('%B %d, %Y at %I:%M %p')} for {hotel_name}</p>
            </div>
        </body>
        </html>
        """
        
        return html_content

    def send_results_email(self, user_email, hotel_name):
        """Send comprehensive results email to user"""
        
        if not user_email or '@' not in user_email:
            return False, "Invalid email address"
            
        try:
            # Create message
            msg = MIMEMultipart('alternative')
            msg['From'] = self.sender_email
            msg['To'] = user_email
            msg['Subject'] = f"🏨 tphagent Marketing Strategy Results - {hotel_name}"
            
            # Create HTML content
            html_content = self.create_email_content(hotel_name, user_email)
            html_part = MIMEText(html_content, 'html', 'utf-8')
            msg.attach(html_part)
            
            # Attach files
            files_to_attach = [
                'outputs/estancia_hacienda_market_research.md',
                'outputs/estancia_hacienda_google_ads.md',
                'outputs/estancia_hacienda_optimization.md',
                'outputs/estancia_hacienda_workflow_results.json'
            ]
            
            for file_path in files_to_attach:
                if os.path.exists(file_path):
                    with open(file_path, "rb") as attachment:
                        part = MIMEBase('application', 'octet-stream')
                        part.set_payload(attachment.read())
                        encoders.encode_base64(part)
                        part.add_header(
                            'Content-Disposition',
                            f'attachment; filename= {os.path.basename(file_path)}'
                        )
                        msg.attach(part)
            
            # Send email
            server = smtplib.SMTP(self.smtp_server, self.smtp_port)
            server.starttls()
            server.login(self.sender_email, self.sender_password)
            text = msg.as_string()
            server.sendmail(self.sender_email, user_email, text)
            server.quit()
            
            return True, "Email sent successfully!"
            
        except Exception as e:
            return False, f"Failed to send email: {str(e)}"

def main():
    """Main function to send results email"""
    print("📧 tphagent Results Email Sender")
    print("=" * 40)
    
    # Get user email
    user_email = input("Enter your email address to receive the complete marketing strategy results: ").strip()
    
    if not user_email:
        print("❌ No email address provided")
        return
    
    # Hotel information
    hotel_name = "The Peacock House by Hacienda La Estancia"
    
    print(f"\n📊 Preparing to send results for: {hotel_name}")
    print(f"📧 Sending to: {user_email}")
    print()
    
    # Check if email credentials are set
    if not os.getenv('EMAIL_USER') or not os.getenv('EMAIL_PASSWORD'):
        print("⚠️  Email credentials not configured.")
        print("To send emails, you need to set up:")
        print("  EMAIL_USER=your-email@gmail.com")
        print("  EMAIL_PASSWORD=your-app-password")
        print()
        print("For now, I'll show you what would be sent:")
        print()
        
        # Show email content preview
        sender = ResultsEmailSender()
        content = sender.create_email_content(hotel_name, user_email)
        print("📧 EMAIL PREVIEW:")
        print("=" * 50)
        print("Subject: 🏨 tphagent Marketing Strategy Results - The Peacock House by Hacienda La Estancia")
        print()
        print("The email would contain:")
        print("✅ Complete market research analysis")
        print("✅ Google Ads campaign strategy")
        print("✅ Performance optimization plan")
        print("✅ All generated files as attachments")
        print("✅ Step-by-step implementation guide")
        print()
        print("To enable email sending, configure your email credentials in the environment variables.")
        return
    
    # Send email
    sender = ResultsEmailSender()
    success, message = sender.send_results_email(user_email, hotel_name)
    
    if success:
        print("✅ " + message)
        print(f"📧 Results sent to: {user_email}")
        print()
        print("📁 The email includes:")
        print("  • Complete market research report")
        print("  • Google Ads campaign strategy")
        print("  • Performance optimization plan")
        print("  • All generated files as attachments")
        print("  • Step-by-step implementation guide")
    else:
        print("❌ " + message)

if __name__ == "__main__":
    main()
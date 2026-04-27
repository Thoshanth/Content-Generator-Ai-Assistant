#!/usr/bin/env python3
"""
Interactive setup script for AI providers
Helps users configure API keys for different providers
"""

import os
import sys
from pathlib import Path

def print_header(title):
    print("\n" + "="*60)
    print(f" {title}")
    print("="*60)

def print_info(msg):
    print(f"ℹ️  {msg}")

def print_success(msg):
    print(f"✅ {msg}")

def print_warning(msg):
    print(f"⚠️  {msg}")

def get_env_path():
    """Get the path to the .env file"""
    return Path(__file__).parent / ".env"

def read_existing_env():
    """Read existing environment variables"""
    env_path = get_env_path()
    env_vars = {}
    
    if env_path.exists():
        with open(env_path, 'r') as f:
            for line in f:
                line = line.strip()
                if line and not line.startswith('#') and '=' in line:
                    key, value = line.split('=', 1)
                    env_vars[key.strip()] = value.strip()
    
    return env_vars

def write_env_file(env_vars):
    """Write environment variables to .env file"""
    env_path = get_env_path()
    
    with open(env_path, 'w') as f:
        f.write("# AI Provider API Keys\n")
        f.write(f"GROQ_API_KEY={env_vars.get('GROQ_API_KEY', '')}\n")
        f.write(f"GEMINI_API_KEY={env_vars.get('GEMINI_API_KEY', '')}\n")
        f.write(f"TOGETHER_API_KEY={env_vars.get('TOGETHER_API_KEY', '')}\n")
        f.write(f"DEEPSEEK_API_KEY={env_vars.get('DEEPSEEK_API_KEY', '')}\n")
        f.write("\n# Service Configuration\n")
        f.write(f"SERVICE_PORT={env_vars.get('SERVICE_PORT', '8000')}\n")
        f.write(f"SERVICE_HOST={env_vars.get('SERVICE_HOST', '0.0.0.0')}\n")

def setup_groq():
    """Setup Groq API key"""
    print_header("Groq Setup (Recommended - Fast & Free)")
    
    print("Groq provides very fast inference with free tier access.")
    print("\n📋 Steps to get Groq API key:")
    print("1. Visit: https://console.groq.com/")
    print("2. Sign up for a free account")
    print("3. Navigate to 'API Keys' section")
    print("4. Create a new API key")
    print("5. Copy the key (starts with 'gsk_')")
    
    key = input("\n🔑 Enter your Groq API key (or press Enter to skip): ").strip()
    
    if key:
        if key.startswith('gsk_'):
            print_success("Groq API key looks valid!")
            return key
        else:
            print_warning("Groq keys usually start with 'gsk_' - double check your key")
            return key
    else:
        print_info("Skipping Groq setup")
        return ""

def setup_gemini():
    """Setup Gemini API key"""
    print_header("Google Gemini Setup (Recommended - Powerful)")
    
    print("Google Gemini provides strong reasoning capabilities with generous free tier.")
    print("\n📋 Steps to get Gemini API key:")
    print("1. Visit: https://aistudio.google.com/")
    print("2. Sign in with your Google account")
    print("3. Click 'Get API key' or 'Create API key'")
    print("4. Copy the generated key")
    
    key = input("\n🔑 Enter your Gemini API key (or press Enter to skip): ").strip()
    
    if key:
        print_success("Gemini API key saved!")
        return key
    else:
        print_info("Skipping Gemini setup")
        return ""

def setup_together():
    """Setup TogetherAI API key"""
    print_header("TogetherAI Setup (Optional - Diverse Models)")
    
    print("TogetherAI offers a wide variety of models with competitive pricing.")
    print("\n📋 Steps to get TogetherAI API key:")
    print("1. Visit: https://api.together.xyz/")
    print("2. Sign up for an account")
    print("3. Go to your dashboard")
    print("4. Generate an API key")
    print("5. Copy the key")
    
    key = input("\n🔑 Enter your TogetherAI API key (or press Enter to skip): ").strip()
    
    if key:
        print_success("TogetherAI API key saved!")
        return key
    else:
        print_info("Skipping TogetherAI setup")
        return ""

def setup_deepseek():
    """Setup DeepSeek API key"""
    print_header("DeepSeek Setup (Optional - Coding Focused)")
    
    print("DeepSeek specializes in coding and technical content generation.")
    print("\n📋 Steps to get DeepSeek API key:")
    print("1. Visit: https://platform.deepseek.com/")
    print("2. Create an account")
    print("3. Navigate to API keys section")
    print("4. Generate a new API key")
    print("5. Copy the key")
    
    key = input("\n🔑 Enter your DeepSeek API key (or press Enter to skip): ").strip()
    
    if key:
        print_success("DeepSeek API key saved!")
        return key
    else:
        print_info("Skipping DeepSeek setup")
        return ""

def main():
    """Main setup function"""
    print_header("AI Content Generator - Provider Setup")
    
    print("This script helps you configure API keys for different AI providers.")
    print("You need at least ONE provider to use the service.")
    print("\n💡 Recommended: Set up Groq (fast) + Gemini (powerful) for best results")
    
    # Read existing configuration
    existing_env = read_existing_env()
    
    if existing_env:
        print_info("Found existing .env file")
        configured_providers = []
        for key in ['GROQ_API_KEY', 'GEMINI_API_KEY', 'TOGETHER_API_KEY', 'DEEPSEEK_API_KEY']:
            if existing_env.get(key):
                provider_name = key.replace('_API_KEY', '').lower()
                configured_providers.append(provider_name)
        
        if configured_providers:
            print_success(f"Already configured: {', '.join(configured_providers)}")
            
            choice = input("\n🔄 Do you want to reconfigure? (y/N): ").strip().lower()
            if choice not in ['y', 'yes']:
                print_info("Keeping existing configuration")
                return
    
    # Setup each provider
    env_vars = existing_env.copy()
    
    # Groq (recommended)
    groq_key = setup_groq()
    if groq_key:
        env_vars['GROQ_API_KEY'] = groq_key
    
    # Gemini (recommended)
    gemini_key = setup_gemini()
    if gemini_key:
        env_vars['GEMINI_API_KEY'] = gemini_key
    
    # Ask if user wants to set up optional providers
    if groq_key or gemini_key:
        print_info("\nYou have at least one provider configured!")
        choice = input("🔧 Do you want to set up additional providers? (y/N): ").strip().lower()
        
        if choice in ['y', 'yes']:
            together_key = setup_together()
            if together_key:
                env_vars['TOGETHER_API_KEY'] = together_key
            
            deepseek_key = setup_deepseek()
            if deepseek_key:
                env_vars['DEEPSEEK_API_KEY'] = deepseek_key
    else:
        # No primary providers, try optional ones
        print_warning("No primary providers configured. Trying optional providers...")
        
        together_key = setup_together()
        if together_key:
            env_vars['TOGETHER_API_KEY'] = together_key
        
        deepseek_key = setup_deepseek()
        if deepseek_key:
            env_vars['DEEPSEEK_API_KEY'] = deepseek_key
    
    # Set default service configuration
    if 'SERVICE_PORT' not in env_vars:
        env_vars['SERVICE_PORT'] = '8000'
    if 'SERVICE_HOST' not in env_vars:
        env_vars['SERVICE_HOST'] = '0.0.0.0'
    
    # Write configuration
    write_env_file(env_vars)
    
    # Summary
    print_header("Setup Complete!")
    
    configured_providers = []
    for key in ['GROQ_API_KEY', 'GEMINI_API_KEY', 'TOGETHER_API_KEY', 'DEEPSEEK_API_KEY']:
        if env_vars.get(key):
            provider_name = key.replace('_API_KEY', '').lower()
            configured_providers.append(provider_name)
    
    if configured_providers:
        print_success(f"Configured providers: {', '.join(configured_providers)}")
        print_info(f"Configuration saved to: {get_env_path()}")
        
        print("\n🚀 Next steps:")
        print("1. Start the service: python main.py")
        print("2. Test providers: python test_providers.py")
        print("3. Run full tests: python test_service.py")
        print("4. Check API docs: http://localhost:8000/docs")
        
    else:
        print_warning("No providers configured!")
        print("You need at least one API key to use the service.")
        print("Run this script again to configure providers.")

if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\n\n⚠️  Setup interrupted by user")
        sys.exit(1)
    except Exception as e:
        print(f"\n❌ Setup failed: {str(e)}")
        sys.exit(2)
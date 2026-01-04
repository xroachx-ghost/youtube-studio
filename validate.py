#!/usr/bin/env python3
"""
Comprehensive validation script for YouTube Studio
Run this to check if everything is properly set up
"""

import sys
import os
import subprocess
from pathlib import Path

def print_header(text):
    print("\n" + "="*60)
    print(text)
    print("="*60)

def main():
    print_header("YouTube Studio - System Validation")
    
    errors = []
    warnings = []
    
    # 1. Check Python version
    print("\n1. Checking Python version...")
    version = sys.version_info
    if version.major >= 3 and version.minor >= 8:
        print(f"  ✅ Python {version.major}.{version.minor}.{version.micro}")
    else:
        errors.append(f"Python 3.8+ required, found {version.major}.{version.minor}")
        print(f"  ❌ Python {version.major}.{version.minor} (3.8+ required)")
    
    # 2. Check Python syntax
    print("\n2. Checking Python files syntax...")
    python_files = [
        'config.py',
        'llm_providers.py',
        'main_free.py',
        'main_premium_free.py',
        'main_ultimate_free.py',
        'youtube_uploader.py',
        'video_generator_gui.py'
    ]
    
    for fname in python_files:
        if not Path(fname).exists():
            warnings.append(f"{fname} not found")
            print(f"  ⚠️  {fname} (not found)")
            continue
            
        try:
            with open(fname) as f:
                compile(f.read(), fname, 'exec')
            print(f"  ✅ {fname}")
        except SyntaxError as e:
            errors.append(f"Syntax error in {fname}: {e}")
            print(f"  ❌ {fname}: {e}")
    
    # 3. Check module imports
    print("\n3. Checking module imports...")
    modules = [
        ('config', 'config.py'),
        ('llm_providers', 'llm_providers.py'),
        ('youtube_uploader', 'youtube_uploader.py'),
        ('main_free', 'main_free.py'),
        ('main_premium_free', 'main_premium_free.py'),
        ('main_ultimate_free', 'main_ultimate_free.py'),
    ]
    
    for module, fname in modules:
        try:
            __import__(module)
            print(f"  ✅ {module}")
        except Exception as e:
            errors.append(f"Import error in {module}: {str(e)[:80]}")
            print(f"  ❌ {module}: {str(e)[:80]}")
    
    # GUI check (set Qt platform only for this import)
    original_qt_platform = os.environ.get('QT_QPA_PLATFORM')
    try:
        os.environ['QT_QPA_PLATFORM'] = 'offscreen'
        import video_generator_gui
        print(f"  ✅ video_generator_gui")
    except Exception as e:
        warnings.append(f"GUI import issue: {str(e)[:80]}")
        print(f"  ⚠️  video_generator_gui: {str(e)[:80]}")
    finally:
        # Restore original Qt platform setting
        if original_qt_platform is not None:
            os.environ['QT_QPA_PLATFORM'] = original_qt_platform
        elif 'QT_QPA_PLATFORM' in os.environ:
            del os.environ['QT_QPA_PLATFORM']
    
    # 4. Check critical dependencies
    print("\n4. Checking Python dependencies...")
    dependencies = [
        ('requests', 'HTTP client library'),
        ('gtts', 'Google Text-to-Speech'),
        ('google.auth', 'Google authentication'),
        ('google_auth_oauthlib', 'OAuth for Google'),
        ('googleapiclient', 'Google API client'),
        ('PyQt5', 'GUI framework')
    ]
    
    for dep, desc in dependencies:
        try:
            __import__(dep)
            print(f"  ✅ {dep:<25} ({desc})")
        except ImportError:
            errors.append(f"Missing dependency: {dep}")
            print(f"  ❌ {dep:<25} ({desc})")
    
    # 5. Check ffmpeg
    print("\n5. Checking ffmpeg (required for video processing)...")
    try:
        result = subprocess.run(['ffmpeg', '-version'], 
                              capture_output=True, 
                              timeout=5)
        if result.returncode == 0:
            version = result.stdout.decode().split('\n')[0]
            print(f"  ✅ {version}")
        else:
            errors.append("ffmpeg not working properly")
            print(f"  ❌ ffmpeg not working")
    except FileNotFoundError:
        errors.append("ffmpeg not found - install with: sudo apt install ffmpeg")
        print(f"  ❌ ffmpeg not found")
    except subprocess.TimeoutExpired:
        errors.append("ffmpeg check timed out")
        print(f"  ❌ ffmpeg check timed out")
    except Exception as e:
        errors.append(f"ffmpeg error: {e}")
        print(f"  ❌ ffmpeg: {e}")
    
    # 6. Check shell scripts
    print("\n6. Checking shell scripts...")
    scripts = [
        'launch_gui.sh',
        'quick_start.sh',
        'setup_all_premium_free.sh',
        'start_menu.sh'
    ]
    
    for script in scripts:
        if Path(script).exists():
            is_executable = os.access(script, os.X_OK)
            if is_executable:
                print(f"  ✅ {script}")
            else:
                warnings.append(f"{script} not executable - run: chmod +x {script}")
                print(f"  ⚠️  {script} (not executable)")
        else:
            warnings.append(f"{script} not found")
            print(f"  ⚠️  {script} (not found)")
    
    # 7. Check environment and directories
    print("\n7. Checking environment...")
    
    if Path('.gitignore').exists():
        print(f"  ✅ .gitignore exists")
    else:
        warnings.append(".gitignore missing")
        print(f"  ⚠️  .gitignore missing")
    
    if Path('output').exists():
        print(f"  ✅ output/ directory exists")
    else:
        print(f"  ℹ️  output/ directory will be created when needed")
    
    # Check for API keys (optional but recommended)
    print("\n8. Checking optional API keys...")
    api_keys = {
        'GEMINI_API_KEY': 'Gemini Pro for AI script generation',
        'OPENAI_API_KEY': 'OpenAI for AI features',
        'PEXELS_API_KEY': 'Pexels for stock videos',
        'PIXABAY_API_KEY': 'Pixabay for stock media',
        'ELEVENLABS_API_KEY': 'ElevenLabs for premium voice',
    }
    
    keys_found = 0
    for key, desc in api_keys.items():
        value = os.getenv(key)
        if value and value.strip():  # Check for non-empty values
            print(f"  ✅ {key:<25} ({desc})")
            keys_found += 1
        else:
            print(f"  ℹ️  {key:<25} (optional - {desc})")
    
    if keys_found == 0:
        print("\n  💡 No API keys configured - app will use free alternatives")
        print("     Set API keys as environment variables to unlock more features")
    
    # Summary
    print_header("VALIDATION SUMMARY")
    
    if errors:
        print(f"\n❌ {len(errors)} CRITICAL ERROR(S) found:")
        for err in errors:
            print(f"  - {err}")
        print("\n🔧 Fix these errors before running the application")
        return 1
    
    if warnings:
        print(f"\n⚠️  {len(warnings)} WARNING(S):")
        for warn in warnings:
            print(f"  - {warn}")
    
    print(f"\n✅ All critical checks passed! The application is ready to run.\n")
    print("📝 NOTES:")
    print("  - Internet connection required for API calls (Google TTS, LLMs, etc.)")
    print("  - API keys are optional but recommended for better features")
    print("  - GUI requires display (use X11 forwarding on remote systems)")
    print("  - Ollama is optional for local LLM script generation")
    print("\n🚀 Quick start:")
    print("  - CLI: python3 main_free.py")
    print("  - GUI: ./launch_gui.sh or python3 video_generator_gui.py")
    print("  - Menu: ./start_menu.sh")
    
    return 0

if __name__ == "__main__":
    sys.exit(main())

"""
Configuration management for the course creator system
"""

import os
import yaml
from typing import Dict, Any, Optional
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

class Config:
    """Configuration class for the course creator system"""
    
    def __init__(self):
        """Initialize configuration"""
        self.test_mode = self._get_test_mode()
        self.api_keys = self._load_api_keys()
        self.output_settings = self._load_output_settings()
        self.ai_settings = self._load_ai_settings()
        self.video_settings = self._load_video_settings()
    
    def _get_test_mode(self) -> bool:
        """Get test mode setting"""
        # Check environment variable first
        test_env = os.getenv('TEST_MODE', '')
        
        test_env_lower = test_env.lower()
        if test_env_lower in ['true', '1', 'yes']:
            return True
        elif test_env_lower in ['false', '0', 'no']:
            return False
        
        # Check config file
        try:
            if os.path.exists('config.yaml'):
                with open('config.yaml', 'r') as f:
                    config_data = yaml.safe_load(f)
                    return config_data.get('test_mode', False)
        except Exception:
            pass
        
        return False
    
    def _load_api_keys(self) -> Dict[str, str]:
        """Load API keys from environment variables"""
        return {
            'openai': os.getenv('OPENAI_API_KEY', ''),
            'did': os.getenv('DID_API_KEY', ''),
            'stability': os.getenv('STABILITY_API_KEY', ''),
            'elevenlabs': os.getenv('ELEVENLABS_API_KEY', '')
        }
    
    def _load_output_settings(self) -> Dict[str, Any]:
        """Load output directory settings"""
        base_dir = 'output_test' if self.test_mode else 'output'
        
        return {
            'base_dir': base_dir,
            'videos': f'{base_dir}/videos',
            'notebooks': f'{base_dir}/notebooks',
            'backgrounds': f'{base_dir}/backgrounds',
            'marketing': f'{base_dir}/marketing',
            'packages': f'{base_dir}/packages'
        }
    
    def get_domain_output_dir(self, domain: str, category: str = None) -> str:
        """Get output directory for specific domain"""
        # Clean domain name for filesystem
        clean_domain = "".join(c for c in domain if c.isalnum() or c in (' ', '-', '_')).strip()
        clean_domain = clean_domain.replace(' ', '_')
        
        base_dir = 'output_test' if self.test_mode else 'output'
        domain_dir = f'{base_dir}/{clean_domain}'
        
        if category:
            return f'{domain_dir}/{category}'
        return domain_dir
    
    def _load_ai_settings(self) -> Dict[str, Any]:
        """Load AI model settings"""
        return {
            'openai_model': 'gpt-4',
            'dalle_model': 'dall-e-3',
            'voice_provider': 'microsoft',
            'default_voice': 'en-US-JennyNeural'
        }
    
    def _load_video_settings(self) -> Dict[str, Any]:
        """Load video generation settings"""
        return {
            'resolution': '1920x1080',
            'fps': 30,
            'quality': 'draft' if self.test_mode else '1080p',
            'max_duration_minutes': 30
        }
    
    def get(self, key: str, default: Any = None) -> Any:
        """Get configuration value by key"""
        keys = key.split('.')
        value = self
        
        for k in keys:
            if isinstance(value, dict) and k in value:
                value = value[k]
            else:
                return default
        
        return value
    
    def is_test_mode(self) -> bool:
        """Check if system is in test mode"""
        return self.test_mode
    
    def get_api_key(self, service: str) -> str:
        """Get API key for specific service"""
        return self.api_keys.get(service, '')
    
    def get_output_dir(self, category: str) -> str:
        """Get output directory for specific category"""
        return self.output_settings.get(category, self.output_settings['base_dir'])
    
    def validate_api_keys(self) -> Dict[str, bool]:
        """Validate all API keys"""
        validation = {}
        
        for service, key in self.api_keys.items():
            if self.test_mode:
                validation[service] = True  # Always valid in test mode
            else:
                validation[service] = bool(key and len(key) > 10)
        
        return validation
    
    def save_config(self, filepath: str = 'config.yaml') -> bool:
        """Save current configuration to file"""
        try:
            config_data = {
                'test_mode': self.test_mode,
                'output_settings': self.output_settings,
                'ai_settings': self.ai_settings,
                'video_settings': self.video_settings
            }
            
            with open(filepath, 'w') as f:
                yaml.dump(config_data, f, default_flow_style=False)
            
            return True
            
        except Exception:
            return False

# Global configuration instance
_config_instance: Optional[Config] = None

def get_config() -> Config:
    """Get global configuration instance"""
    global _config_instance
    
    if _config_instance is None:
        _config_instance = Config()
    
    return _config_instance

def reload_config() -> Config:
    """Reload configuration from files"""
    global _config_instance
    
    _config_instance = Config()
    return _config_instance 

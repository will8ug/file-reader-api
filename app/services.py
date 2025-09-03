import json
import os
from pathlib import Path
from typing import List, Optional
from .models import PromptMetadata, PromptTemplate


class PromptService:
    def __init__(self, resources_dir: str = "resources/prompts"):
        self.resources_dir = Path(resources_dir)
    
    def _get_metadata_files(self) -> List[str]:
        """Automatically discover all JSON metadata files in the resources directory."""
        metadata_files = []
        if self.resources_dir.exists():
            for file_path in self.resources_dir.glob("*.json"):
                metadata_files.append(file_path.name)
        return metadata_files
    
    def get_all_prompts(self) -> List[PromptMetadata]:
        """Get metadata for all prompts without file content."""
        all_prompts = []
        metadata_files = self._get_metadata_files()
        
        for metadata_file in metadata_files:
            file_path = self.resources_dir / metadata_file
            if file_path.exists():
                try:
                    with open(file_path, 'r', encoding='utf-8') as f:
                        prompts_data = json.load(f)
                        for prompt_data in prompts_data:
                            all_prompts.append(PromptMetadata(**prompt_data))
                except (json.JSONDecodeError, KeyError) as e:
                    print(f"Error reading metadata file {metadata_file}: {e}")
                    continue
        
        return all_prompts
    
    def get_prompt_by_code(self, code: int) -> Optional[PromptTemplate]:
        """Get a specific prompt template by code, including file content."""
        all_prompts = self.get_all_prompts()
        
        for prompt_metadata in all_prompts:
            if prompt_metadata.code == code:
                # Read the file content
                content_file_path = self.resources_dir / prompt_metadata.file
                if content_file_path.exists():
                    try:
                        with open(content_file_path, 'r', encoding='utf-8') as f:
                            content = f.read().strip()
                        
                        # Create PromptTemplate without the 'file' field
                        return PromptTemplate(
                            name=prompt_metadata.name,
                            code=prompt_metadata.code,
                            scope=prompt_metadata.scope,
                            params=prompt_metadata.params,
                            content=content
                        )
                    except Exception as e:
                        print(f"Error reading content file {prompt_metadata.file}: {e}")
                        continue
        
        return None

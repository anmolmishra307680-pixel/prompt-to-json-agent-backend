import re
from typing import Dict, List, Optional

class AdvancedNLPParser:
    """Unified advanced NLP parser with semantic understanding and multi-language support"""
    
    def __init__(self):
        self.type_embeddings = {
            "building": ["building", "house", "office", "library", "structure", "construction", "architecture", "tower", "skyscraper", "warehouse",
                        "casa", "edificio", "oficina", "maison", "bâtiment", "bureau", "haus", "gebäude", "büro"],
            "car": ["car", "vehicle", "automobile", "sports car", "racing car", "sedan", "suv", "truck", "van", "coupe",
                   "coche", "auto", "vehículo", "voiture", "automobile", "véhicule", "auto", "fahrzeug", "wagen"],
            "drone": ["drone", "uav", "aircraft", "flying", "quadcopter", "helicopter", "aerial", "unmanned", "copter",
                     "dron", "avión", "helicóptero", "drone", "avion", "hélicoptère", "drohne", "flugzeug", "hubschrauber"],
            "table": ["table", "desk", "furniture", "dining table", "coffee table", "workbench", "surface",
                     "mesa", "escritorio", "mueble", "table", "bureau", "meuble", "tisch", "schreibtisch", "möbel"],
            "gearbox": ["gearbox", "gear", "transmission", "mechanical", "engine part", "drivetrain", "clutch",
                       "caja de cambios", "engranaje", "transmisión", "boîte de vitesses", "engrenage", "transmission", "getriebe", "zahnrad"]
        }
        
        self.material_context = {
            "automotive": ["steel", "aluminum", "carbon fiber", "plastic", "rubber", "glass"],
            "construction": ["concrete", "steel", "wood", "glass", "brick", "stone"],
            "aerospace": ["carbon fiber", "aluminum", "titanium", "composite"],
            "furniture": ["wood", "metal", "glass", "plastic", "fabric"]
        }
        
        self.color_translations = {
            "red": ["red", "rojo", "rouge", "rot"],
            "blue": ["blue", "azul", "bleu", "blau"],
            "green": ["green", "verde", "vert", "grün"],
            "black": ["black", "negro", "noir", "schwarz"],
            "white": ["white", "blanco", "blanc", "weiß"],
            "yellow": ["yellow", "amarillo", "jaune", "gelb"]
        }
    
    def extract_type_with_confidence(self, prompt: str) -> Dict[str, float]:
        """Extract object type with confidence scores"""
        prompt_lower = prompt.lower()
        scores = {}
        
        for obj_type, keywords in self.type_embeddings.items():
            score = 0
            for keyword in keywords:
                if keyword in prompt_lower:
                    # Weight longer keywords higher
                    score += len(keyword.split()) * 2
                    # Boost exact matches
                    if f" {keyword} " in f" {prompt_lower} ":
                        score += 3
            
            if score > 0:
                scores[obj_type] = score
        
        return scores
    
    def extract_materials_contextual(self, prompt: str, obj_type: str) -> List[str]:
        """Extract materials with contextual understanding"""
        prompt_lower = prompt.lower()
        materials = []
        
        # Material keywords with synonyms
        material_patterns = {
            "steel": ["steel", "metal", "iron", "stainless"],
            "aluminum": ["aluminum", "aluminium", "alloy", "lightweight metal"],
            "wood": ["wood", "wooden", "timber", "oak", "pine", "mahogany", "bamboo"],
            "concrete": ["concrete", "cement", "reinforced concrete"],
            "glass": ["glass", "transparent", "tempered glass", "laminated"],
            "carbon fiber": ["carbon fiber", "carbon fibre", "composite", "lightweight"],
            "plastic": ["plastic", "polymer", "abs", "pvc", "synthetic"],
            "brick": ["brick", "masonry", "clay brick"],
            "stone": ["stone", "granite", "marble", "limestone", "rock"]
        }
        
        # Extract mentioned materials
        for material, patterns in material_patterns.items():
            for pattern in patterns:
                if pattern in prompt_lower:
                    materials.append(material)
                    break
        
        # Context-based suggestions if no materials found
        if not materials:
            context_map = {
                "car": ["aluminum", "steel"],
                "building": ["concrete", "glass"],
                "drone": ["carbon fiber", "aluminum"],
                "table": ["wood", "metal"],
                "gearbox": ["steel", "aluminum"]
            }
            materials = context_map.get(obj_type, ["steel"])
        
        return list(dict.fromkeys(materials))  # Remove duplicates while preserving order
    
    def extract_dimensions_advanced(self, prompt: str) -> Optional[str]:
        """Advanced dimension extraction with multiple patterns"""
        patterns = [
            r'(\d+(?:\.\d+)?)\s*[x×]\s*(\d+(?:\.\d+)?)\s*[x×]\s*(\d+(?:\.\d+)?)\s*([a-zA-Z]+)',  # 3D with unit
            r'(\d+(?:\.\d+)?)\s*[x×]\s*(\d+(?:\.\d+)?)\s*([a-zA-Z]+)',  # 2D with unit
            r'(\d+(?:\.\d+)?)\s*[x×]\s*(\d+(?:\.\d+)?)\s*[x×]\s*(\d+(?:\.\d+)?)',  # 3D no unit
            r'(\d+(?:\.\d+)?)\s*[x×]\s*(\d+(?:\.\d+)?)',  # 2D no unit
            r'(\d+(?:\.\d+)?)\s*(meters?|metres?|m)\s*[x×]\s*(\d+(?:\.\d+)?)\s*(meters?|metres?|m)',  # Verbose
            r'(\d+(?:\.\d+)?)\s*(cm|centimeters?)\s*[x×]\s*(\d+(?:\.\d+)?)\s*(cm|centimeters?)'  # CM verbose
        ]
        
        for pattern in patterns:
            match = re.search(pattern, prompt, re.IGNORECASE)
            if match:
                groups = match.groups()
                if len(groups) >= 4 and groups[3].isalpha():  # 3D with unit
                    return f"{groups[0]}x{groups[1]}x{groups[2]}{groups[3]}"
                elif len(groups) == 3 and groups[2].isalpha():  # 2D with unit
                    return f"{groups[0]}x{groups[1]}{groups[2]}"
                elif len(groups) == 3:  # 3D no unit
                    return f"{groups[0]}x{groups[1]}x{groups[2]}m"
                elif len(groups) >= 4:  # Verbose patterns
                    unit = groups[1] if groups[1] else groups[3]
                    return f"{groups[0]}x{groups[2]}{unit[0]}"
                else:  # 2D no unit
                    return f"{groups[0]}x{groups[1]}m"
        
        return None
    
    def extract_purpose_semantic(self, prompt: str) -> Optional[str]:
        """Extract purpose with semantic understanding"""
        purpose_patterns = [
            r'for\s+([^,.]+)',
            r'used\s+for\s+([^,.]+)',
            r'designed\s+for\s+([^,.]+)',
            r'intended\s+for\s+([^,.]+)',
            r'purpose\s+is\s+([^,.]+)'
        ]
        
        for pattern in purpose_patterns:
            match = re.search(pattern, prompt, re.IGNORECASE)
            if match:
                return match.group(1).strip()
        
        return None
    
    def parse_prompt(self, prompt: str) -> Dict:
        """Parse prompt with unified advanced NLP and semantic analysis"""
        # Enhanced type detection with confidence
        type_scores = self.extract_type_with_confidence(prompt)
        obj_type = max(type_scores, key=type_scores.get) if type_scores else "unknown"
        confidence = type_scores.get(obj_type, 0)
        
        # Contextual attribute extraction
        materials = self.extract_materials_contextual(prompt, obj_type)
        dimensions = self.extract_dimensions_advanced(prompt)
        purpose = self.extract_purpose_semantic(prompt)
        color = self._extract_color_multilingual(prompt)
        
        # Advanced semantic validation
        if confidence < 3 and obj_type != "unknown":
            obj_type = "unknown"
            confidence = 0
        
        return {
            "type": obj_type,
            "material": materials,
            "dimensions": dimensions,
            "color": color,
            "purpose": purpose,
            "extras": None,
            "confidence": confidence,
            "semantic_quality": self._assess_semantic_quality(prompt, obj_type, materials)
        }
    
    def _extract_color_multilingual(self, prompt: str) -> Optional[str]:
        """Extract color with multi-language support"""
        for eng_color, translations in self.color_translations.items():
            for color_word in translations:
                if color_word in prompt.lower():
                    return eng_color
        return None
    
    def _assess_semantic_quality(self, prompt: str, obj_type: str, materials: List[str]) -> float:
        """Assess semantic understanding quality"""
        quality = 0.5  # Base quality
        if obj_type != "unknown": quality += 0.3
        if materials and materials != ["unknown"]: quality += 0.2
        if len(prompt.split()) > 3: quality += 0.1  # Detailed prompts
        return min(1.0, quality)
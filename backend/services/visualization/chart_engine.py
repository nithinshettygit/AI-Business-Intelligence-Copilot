import json
import plotly.express as px
import plotly.graph_objects as go
import pandas as pd
from typing import Dict, Any, Optional

class VisualizationEngine:
    def __init__(self):
        pass
        
    def generate_chart_config(self, df_dict: Dict[str, Any], chart_type: str, x_col: str, y_col: str, title: str = "") -> Optional[Dict[str, Any]]:
        """
        Generates a Plotly JSON configuration from an aggregated dictionary/dataframe.
        The frontend will render this config natively using streamlit-plotly.
        """
        try:
            # Reconstruct dataframe from result dictionary if possible
            if isinstance(df_dict, dict):
                # Simple single-row dict -> bar chart of keys and values
                if len(df_dict) > 0 and all(isinstance(v, (int, float)) for v in df_dict.values()):
                    df = pd.DataFrame(list(df_dict.items()), columns=[x_col, y_col])
                else:
                    df = pd.DataFrame(df_dict)
            else:
                df = df_dict
                
            if chart_type == "bar":
                fig = px.bar(df, x=x_col, y=y_col, title=title, template="plotly_dark")
            elif chart_type == "line":
                fig = px.line(df, x=x_col, y=y_col, title=title, template="plotly_dark")
            elif chart_type == "pie":
                fig = px.pie(df, names=x_col, values=y_col, title=title, template="plotly_dark")
            elif chart_type == "scatter":
                fig = px.scatter(df, x=x_col, y=y_col, title=title, template="plotly_dark")
            else:
                # Default back to bar
                fig = px.bar(df, x=x_col, y=y_col, title=title, template="plotly_dark")
                
            # Convert to dict for JSON serialization over the API
            return json.loads(fig.to_json())
            
        except Exception as e:
            print(f"Error generating chart: {e}")
            return None

visualization_engine = VisualizationEngine()

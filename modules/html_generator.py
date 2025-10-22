#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
HTML生成モジュール

D3.jsまたはCytoscape.jsを使用してエコマップのHTMLを生成します。
"""

from typing import Dict, Any
import json


class HTMLGenerator:
    """HTML生成クラス"""
    
    def __init__(self, visualization: str = "d3"):
        """
        初期化
        
        Args:
            visualization: 可視化ライブラリ（"d3" or "cytoscape"）
        """
        self.visualization = visualization
    
    def generate(self, json_data: Dict[str, Any], person_name: str) -> str:
        """
        HTMLを生成
        
        Args:
            json_data: JSONデータ
            person_name: 本人氏名
            
        Returns:
            HTML文字列
        """
        if self.visualization == "d3":
            return self._generate_d3_html(json_data, person_name)
        elif self.visualization == "cytoscape":
            return self._generate_cytoscape_html(json_data, person_name)
        else:
            raise ValueError(f"不明な可視化ライブラリ: {self.visualization}")
    
    def _generate_d3_html(self, json_data: Dict[str, Any], person_name: str) -> str:
        """
        D3.jsを使用したHTMLを生成
        
        Args:
            json_data: JSONデータ
            person_name: 本人氏名
            
        Returns:
            HTML文字列
        """
        # JSONデータをJavaScript用にエスケープ
        json_str = json.dumps(json_data, ensure_ascii=False, indent=2)
        
        html = f"""<!DOCTYPE html>
<html lang="ja">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>エコマップ - {person_name}</title>
    <script src="https://d3js.org/d3.v7.min.js"></script>
    <style>
        body {{
            font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
            margin: 0;
            padding: 20px;
            background-color: #f5f5f5;
        }}
        
        #container {{
            max-width: 1400px;
            margin: 0 auto;
            background-color: white;
            border-radius: 8px;
            box-shadow: 0 2px 10px rgba(0,0,0,0.1);
        }}
        
        #header {{
            padding: 20px 30px;
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            color: white;
            border-radius: 8px 8px 0 0;
        }}
        
        h1 {{
            margin: 0 0 10px 0;
            font-size: 28px;
        }}
        
        .subtitle {{
            margin: 0;
            opacity: 0.9;
            font-size: 14px;
        }}
        
        #controls {{
            padding: 20px 30px;
            border-bottom: 1px solid #e0e0e0;
            background-color: #fafafa;
        }}
        
        .control-group {{
            margin-bottom: 15px;
        }}
        
        .control-group:last-child {{
            margin-bottom: 0;
        }}
        
        .control-label {{
            font-weight: 600;
            margin-bottom: 8px;
            display: block;
            color: #333;
        }}
        
        .checkbox-group {{
            display: flex;
            flex-wrap: wrap;
            gap: 15px;
        }}
        
        .checkbox-item {{
            display: flex;
            align-items: center;
        }}
        
        .checkbox-item input[type="checkbox"] {{
            margin-right: 5px;
            cursor: pointer;
        }}
        
        .checkbox-item label {{
            cursor: pointer;
            user-select: none;
        }}
        
        #ecomap {{
            width: 100%;
            height: 700px;
            border-radius: 0 0 8px 8px;
        }}
        
        .node {{
            cursor: pointer;
            stroke: #fff;
            stroke-width: 2px;
        }}
        
        .node:hover {{
            stroke: #333;
            stroke-width: 3px;
        }}
        
        .link {{
            stroke-opacity: 0.6;
        }}
        
        .label {{
            font-size: 12px;
            pointer-events: none;
            text-shadow: 0 1px 2px rgba(255,255,255,0.8);
        }}
        
        .tooltip {{
            position: absolute;
            padding: 12px;
            background: rgba(0, 0, 0, 0.9);
            color: white;
            border-radius: 4px;
            pointer-events: none;
            font-size: 13px;
            max-width: 300px;
            box-shadow: 0 2px 10px rgba(0,0,0,0.3);
            z-index: 1000;
        }}
        
        .tooltip-title {{
            font-weight: 600;
            margin-bottom: 5px;
            border-bottom: 1px solid rgba(255,255,255,0.3);
            padding-bottom: 5px;
        }}
        
        .tooltip-content {{
            font-size: 12px;
            line-height: 1.5;
        }}
    </style>
</head>
<body>
    <div id="container">
        <div id="header">
            <h1>エコマップ - {person_name}</h1>
            <p class="subtitle">支援関係図</p>
        </div>
        
        <div id="controls">
            <div class="control-group">
                <div class="control-label">表示レイヤー</div>
                <div class="checkbox-group">
                    <div class="checkbox-item">
                        <input type="checkbox" id="layer-person" checked disabled>
                        <label for="layer-person">本人</label>
                    </div>
                    <div class="checkbox-item">
                        <input type="checkbox" id="layer-family" checked>
                        <label for="layer-family">家族</label>
                    </div>
                    <div class="checkbox-item">
                        <input type="checkbox" id="layer-notebooks" checked>
                        <label for="layer-notebooks">手帳</label>
                    </div>
                    <div class="checkbox-item">
                        <input type="checkbox" id="layer-support_levels" checked>
                        <label for="layer-support_levels">支援区分</label>
                    </div>
                    <div class="checkbox-item">
                        <input type="checkbox" id="layer-diagnoses">
                        <label for="layer-diagnoses">診断</label>
                    </div>
                    <div class="checkbox-item">
                        <input type="checkbox" id="layer-legal_guardians" checked>
                        <label for="layer-legal_guardians">成年後見</label>
                    </div>
                    <div class="checkbox-item">
                        <input type="checkbox" id="layer-consultation_supports">
                        <label for="layer-consultation_supports">相談支援</label>
                    </div>
                    <div class="checkbox-item">
                        <input type="checkbox" id="layer-service_plans" checked>
                        <label for="layer-service_plans">利用計画</label>
                    </div>
                    <div class="checkbox-item">
                        <input type="checkbox" id="layer-service_contracts" checked>
                        <label for="layer-service_contracts">サービス契約</label>
                    </div>
                    <div class="checkbox-item">
                        <input type="checkbox" id="layer-medical">
                        <label for="layer-medical">医療</label>
                    </div>
                </div>
            </div>
        </div>
        
        <svg id="ecomap"></svg>
    </div>
    
    <script>
        // データをロード
        const data = {json_str};
        
        // SVG設定
        const width = document.getElementById('ecomap').clientWidth;
        const height = 700;
        
        const svg = d3.select('#ecomap')
            .attr('width', width)
            .attr('height', height);
        
        // ツールチップ
        const tooltip = d3.select('body')
            .append('div')
            .attr('class', 'tooltip')
            .style('opacity', 0);
        
        // Force Simulationの設定
        const simulation = d3.forceSimulation(data.nodes)
            .force('link', d3.forceLink(data.relations).id(d => d.id).distance(150))
            .force('charge', d3.forceManyBody().strength(-400))
            .force('center', d3.forceCenter(width / 2, height / 2))
            .force('collision', d3.forceCollide().radius(d => getSizeValue(d.display.size) + 10));
        
        // ノードサイズの変換
        function getSizeValue(size) {{
            if (size === 'large') return 40;
            if (size === 'medium') return 25;
            if (size === 'small') return 15;
            return 25;
        }}
        
        // 色の変換
        function getColorValue(color) {{
            const colorMap = {{
                'orange': '#FF6B35',
                'red': '#E63946',
                'darkred': '#9D0208',
                'darkgreen': '#2D6A4F',
                'darkblue': '#1D3557',
                'purple': '#7209B7',
                'lightblue': '#4CC9F0',
                'brown': '#8B4513',
                'blue': '#4361EE',
                'blueviolet': '#7209B7',
                'green': '#52B788',
                'gray': '#6C757D',
                'pink': '#FF6B9D'
            }};
            return colorMap[color] || color;
        }}
        
        // リンクの描画
        const link = svg.append('g')
            .selectAll('line')
            .data(data.relations)
            .enter().append('line')
            .attr('class', 'link')
            .attr('stroke', d => d.display.color)
            .attr('stroke-width', d => d.display.line_width)
            .attr('stroke-dasharray', d => d.display.line_style === 'dashed' ? '5,5' : '0')
            .attr('marker-end', d => d.display.arrow ? 'url(#arrow)' : '');
        
        // 矢印マーカーの定義
        svg.append('defs').append('marker')
            .attr('id', 'arrow')
            .attr('viewBox', '0 -5 10 10')
            .attr('refX', 20)
            .attr('refY', 0)
            .attr('markerWidth', 6)
            .attr('markerHeight', 6)
            .attr('orient', 'auto')
            .append('path')
            .attr('d', 'M0,-5L10,0L0,5')
            .attr('fill', '#999');
        
        // ノードの描画
        const node = svg.append('g')
            .selectAll('circle')
            .data(data.nodes)
            .enter().append('circle')
            .attr('class', 'node')
            .attr('r', d => getSizeValue(d.display.size))
            .attr('fill', d => getColorValue(d.display.color))
            .on('mouseover', function(event, d) {{
                // ツールチップ表示
                let content = `<div class="tooltip-title">${{d.name}}</div>`;
                content += `<div class="tooltip-content">`;
                content += `タイプ: ${{d.type}}<br>`;
                content += `レイヤー: ${{d.layer}}<br>`;
                if (d.properties.age) {{
                    content += `年齢: ${{d.properties.age}}歳<br>`;
                }}
                content += `</div>`;
                
                tooltip.transition()
                    .duration(200)
                    .style('opacity', .9);
                tooltip.html(content)
                    .style('left', (event.pageX + 10) + 'px')
                    .style('top', (event.pageY - 28) + 'px');
            }})
            .on('mouseout', function(d) {{
                tooltip.transition()
                    .duration(500)
                    .style('opacity', 0);
            }})
            .call(d3.drag()
                .on('start', dragstarted)
                .on('drag', dragged)
                .on('end', dragended));
        
        // ラベルの描画
        const label = svg.append('g')
            .selectAll('text')
            .data(data.nodes)
            .enter().append('text')
            .attr('class', 'label')
            .attr('dx', 12)
            .attr('dy', 4)
            .text(d => d.display.label);
        
        // Simulationの更新
        simulation.on('tick', () => {{
            link
                .attr('x1', d => d.source.x)
                .attr('y1', d => d.source.y)
                .attr('x2', d => d.target.x)
                .attr('y2', d => d.target.y);
            
            node
                .attr('cx', d => d.x)
                .attr('cy', d => d.y);
            
            label
                .attr('x', d => d.x)
                .attr('y', d => d.y);
        }});
        
        // ドラッグ関数
        function dragstarted(event, d) {{
            if (!event.active) simulation.alphaTarget(0.3).restart();
            d.fx = d.x;
            d.fy = d.y;
        }}
        
        function dragged(event, d) {{
            d.fx = event.x;
            d.fy = event.y;
        }}
        
        function dragended(event, d) {{
            if (!event.active) simulation.alphaTarget(0);
            d.fx = null;
            d.fy = null;
        }}
        
        // レイヤー制御
        function toggleLayer(layer) {{
            // ノードの表示/非表示
            node.style('display', d => {{
                if (d.layer === layer) {{
                    return document.getElementById(`layer-${{layer}}`).checked ? 'block' : 'none';
                }}
                return null;
            }});
            
            label.style('display', d => {{
                if (d.layer === layer) {{
                    return document.getElementById(`layer-${{layer}}`).checked ? 'block' : 'none';
                }}
                return null;
            }});
            
            // リンクの表示/非表示
            link.style('display', d => {{
                const sourceVisible = node.filter(n => n.id === d.source.id).style('display') !== 'none';
                const targetVisible = node.filter(n => n.id === d.target.id).style('display') !== 'none';
                return (sourceVisible && targetVisible) ? 'block' : 'none';
            }});
        }}
        
        // レイヤーチェックボックスのイベント
        document.querySelectorAll('input[type="checkbox"]').forEach(checkbox => {{
            if (checkbox.id !== 'layer-person') {{
                checkbox.addEventListener('change', function() {{
                    const layer = this.id.replace('layer-', '');
                    toggleLayer(layer);
                }});
            }}
        }});
        
        // 初期表示
        ['diagnoses', 'consultation_supports', 'medical'].forEach(layer => {{
            toggleLayer(layer);
        }});
    </script>
</body>
</html>"""
        
        return html
    
    def _generate_cytoscape_html(self, json_data: Dict[str, Any], person_name: str) -> str:
        """
        Cytoscape.jsを使用したHTMLを生成
        
        Args:
            json_data: JSONデータ
            person_name: 本人氏名
            
        Returns:
            HTML文字列
        """
        # TODO: Cytoscape.js版の実装
        # 現時点ではD3.js版を返す
        return self._generate_d3_html(json_data, person_name)


if __name__ == "__main__":
    print("=== HTMLGenerator テスト ===")
    
    # テスト用の簡単なデータ
    test_data = {
        "person": {
            "id": "person-1",
            "name": "山田太郎",
            "age": 25
        },
        "nodes": [
            {
                "id": "person-1",
                "type": "Person",
                "name": "山田太郎",
                "properties": {"age": 25},
                "display": {"color": "orange", "size": "large", "label": "山田太郎"},
                "layer": "person",
                "is_default_visible": True
            },
            {
                "id": "family-1",
                "type": "Family",
                "name": "山田花子",
                "properties": {"relation": "母"},
                "display": {"color": "red", "size": "medium", "label": "山田花子"},
                "layer": "family",
                "is_default_visible": True
            }
        ],
        "relations": [
            {
                "id": "rel-1",
                "type": "FAMILY_RELATION",
                "source_id": "person-1",
                "target_id": "family-1",
                "properties": {"relation": "母"},
                "direction": "undirected",
                "display": {
                    "line_style": "solid",
                    "line_width": 2,
                    "color": "#999",
                    "arrow": False
                },
                "layer": "family"
            }
        ],
        "metadata": {
            "created_at": "2025-10-21T12:00:00",
            "node_count": 2,
            "relation_count": 1
        }
    }
    
    generator = HTMLGenerator("d3")
    html = generator.generate(test_data, "山田太郎")
    
    # HTMLをファイルに保存
    with open("/tmp/test_ecomap.html", "w", encoding="utf-8") as f:
        f.write(html)
    
    print("テスト用HTMLを生成しました: /tmp/test_ecomap.html")
    print(f"HTMLサイズ: {len(html)} 文字")

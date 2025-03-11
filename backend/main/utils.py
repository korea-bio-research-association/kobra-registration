import docx
from docx.enum.text import WD_ALIGN_PARAGRAPH
from docx.text.hyperlink import Hyperlink

import zipfile
import xml.etree.ElementTree as ET

def __process_run(r, p):
    p_bold = p.style.font.bold
    p_italic = p.style.font.italic
    p_underline = p.style.font.underline
    p_subscript = p.style.font.subscript
    p_superscript = p.style.font.superscript
    
    if hasattr(r, 'font'):
        r_bold = r.font.bold if r.font.bold is not None else p_bold
        r_italic = r.font.italic if r.font.italic is not None else p_italic
        r_underline = r.font.underline if r.font.underline is not None else p_underline
        r_subscript = r.font.subscript if r.font.subscript is not None else p_subscript
        r_superscript = r.font.superscript if r.font.superscript is not None else p_superscript
    else:
        r_bold = p_bold
        r_italic = p_italic
        r_underline = p_underline
        r_subscript = p_subscript
        r_superscript = p_superscript
        
    r_text = r.text
    if r_bold:
        r_text = f'<b>{r_text}</b>'
    if r_italic:
        r_text = f'<i>{r_text}</i>'
    if r_underline:
        r_text = f'<u>{r_text}</u>'
    if r_subscript:
        r_text = f'<sub>{r_text}</sub>'
    if r_superscript:
        r_text = f'<sup>{r_text}</sup>'
    return r_text

def docx_to_html(file_path):
    """
    Convert a DOCX document to HTML focusing only on basic formatting:
    - Paragraph alignment
    - Bold, italic, underline
    - Superscript, subscript
    
    Args:
        file_path (str): Path to the DOCX file
        
    Returns:
        str: HTML content of the document
    """

    doc = docx.Document(file_path)
    html = ''
    for p in doc.paragraphs:
        p_alignment = 'left'
        if p.style.paragraph_format.alignment is not None:
            p_alignment = p.style.paragraph_format.alignment
        if p.alignment is not None:
            p_alignment = p.alignment
        if p_alignment == WD_ALIGN_PARAGRAPH.LEFT:
            p_alignment = 'left'
        elif p_alignment == WD_ALIGN_PARAGRAPH.CENTER:
            p_alignment = 'center'
        elif p_alignment == WD_ALIGN_PARAGRAPH.RIGHT:
            p_alignment = 'right'
        elif p_alignment == WD_ALIGN_PARAGRAPH.JUSTIFY:
            p_alignment = 'justify'
        html += f'<p class="docx_paragraphs" style="text-align: {p_alignment};">'
        for r_or_h in p.iter_inner_content():
            if isinstance(r_or_h, Hyperlink):
                for r in r_or_h.runs:
                    html += __process_run(r, p)
            else:
                html += __process_run(r_or_h, p)
        html += '</p>'
    return html

def __resolve_style(style_name, style_dict, style_hierarchy_dict, other_style_dict=None):
    """
    Recursively resolve a style by following the entire inheritance chain
    
    Args:
        style_name: The name of the style to resolve
        style_dict: Dictionary containing styles (either styles or automatic_styles)
        style_hierarchy_dict: Dictionary mapping style names to their parent style names
        other_style_dict: Optional secondary style dictionary to check (for cross-dictionary inheritance)
        
    Returns:
        dict: Fully resolved style properties
    """
    if style_name not in style_dict and (other_style_dict is None or style_name not in other_style_dict):
        return {}
        
    # Start with base style properties
    resolved_style = {}
    
    # First check if style exists in primary dictionary
    if style_name in style_dict:
        # Get parent style name if it exists
        parent_name = style_hierarchy_dict.get(style_name)
        
        if parent_name:
            # First check if parent is in the same dictionary
            if parent_name in style_dict:
                # Recursively resolve parent style first
                parent_style = __resolve_style(parent_name, style_dict, style_hierarchy_dict, other_style_dict)
                resolved_style.update(parent_style)
            # Then check if parent is in the other dictionary (if provided)
            elif other_style_dict and parent_name in other_style_dict:
                # For cross-dictionary inheritance (e.g., automatic style inheriting from document style)
                parent_style = __resolve_style(parent_name, other_style_dict, 
                                               {k: v for k, v in style_hierarchy_dict.items() if k in other_style_dict})
                resolved_style.update(parent_style)
        
        # Add this style's properties (overriding any inherited properties)
        resolved_style.update(style_dict[style_name])
        
    # If not in primary dictionary but in secondary, use that
    elif other_style_dict and style_name in other_style_dict:
        # For styles that only exist in the other dictionary
        resolved_style = __resolve_style(style_name, other_style_dict, 
                                         {k: v for k, v in style_hierarchy_dict.items() if k in other_style_dict})
        
    return resolved_style

def odt_to_html(file_path):
    """
    Convert an ODT document to HTML focusing only on basic formatting:
    - Paragraph alignment
    - Bold, italic, underline
    - Superscript, subscript
    
    Args:
        file_path (str): Path to the ODT file
        
    Returns:
        str: HTML content of the document
    """
    # ODT namespaces
    namespaces = {
        'office': 'urn:oasis:names:tc:opendocument:xmlns:office:1.0',
        'style': 'urn:oasis:names:tc:opendocument:xmlns:style:1.0',
        'text': 'urn:oasis:names:tc:opendocument:xmlns:text:1.0',
        'fo': 'urn:oasis:names:tc:opendocument:xmlns:xsl-fo-compatible:1.0',
    }
    
    # Dictionary to store styles (focus only on key formatting)
    styles = {}
    automatic_styles = {}
    
    # Open the ODT file as a zip archive
    with zipfile.ZipFile(file_path, 'r') as odt_file:
        # Extract and parse styles.xml
        if 'styles.xml' in odt_file.namelist():
            styles_content = odt_file.read('styles.xml')
            styles_root = ET.fromstring(styles_content)
            
            # Get style hierarchies (map of style name to parent style name)
            style_hierarchy = {}
            
            for style_elem in styles_root.findall('.//style:style', namespaces):
                style_name = style_elem.get('{{{0}}}name'.format(namespaces['style']))
                style_properties = {}
                
                # Get parent style name if it exists
                parent_style_name = style_elem.get('{{{0}}}parent-style-name'.format(namespaces['style']))
                if parent_style_name:
                    style_hierarchy[style_name] = parent_style_name
                
                # Paragraph properties (for alignment)
                para_prop = style_elem.find('.//style:paragraph-properties', namespaces)
                if para_prop is not None:
                    # Only extract alignment
                    fo_align = '{{{0}}}text-align'.format(namespaces['fo'])
                    if fo_align in para_prop.attrib:
                        style_properties[fo_align] = para_prop.attrib[fo_align]
                
                # Text properties (bold, italic, etc.)
                text_prop = style_elem.find('.//style:text-properties', namespaces)
                if text_prop is not None:
                    # Extract only bold, italic, underline, position (for sub/superscript)
                    fo_weight = '{{{0}}}font-weight'.format(namespaces['fo'])
                    fo_style = '{{{0}}}font-style'.format(namespaces['fo'])
                    style_underline = '{{{0}}}text-underline-style'.format(namespaces['style'])
                    style_position = '{{{0}}}text-position'.format(namespaces['style'])
                    
                    for attr_name in [fo_weight, fo_style, style_underline, style_position]:
                        if attr_name in text_prop.attrib:
                            style_properties[attr_name] = text_prop.attrib[attr_name]
                
                styles[style_name] = style_properties
        
        # Extract and parse content.xml
        content = odt_file.read('content.xml')
        root = ET.fromstring(content)
        
        # Get automatic style hierarchy
        auto_style_hierarchy = {}
        
        for auto_style in root.findall('.//office:automatic-styles/style:style', namespaces):
            style_name = auto_style.get('{{{0}}}name'.format(namespaces['style']))
            style_properties = {}
            
            # Get parent style name if it exists
            parent_style_name = auto_style.get('{{{0}}}parent-style-name'.format(namespaces['style']))
            if parent_style_name:
                auto_style_hierarchy[style_name] = parent_style_name
            
            # Paragraph properties (for alignment)
            para_prop = auto_style.find('.//style:paragraph-properties', namespaces)
            if para_prop is not None:
                # Only extract alignment
                fo_align = '{{{0}}}text-align'.format(namespaces['fo'])
                if fo_align in para_prop.attrib:
                    style_properties[fo_align] = para_prop.attrib[fo_align]
            
            # Text properties (bold, italic, etc.)
            text_prop = auto_style.find('.//style:text-properties', namespaces)
            if text_prop is not None:
                # Extract only bold, italic, underline, position (for sub/superscript)
                fo_weight = '{{{0}}}font-weight'.format(namespaces['fo'])
                fo_style = '{{{0}}}font-style'.format(namespaces['fo'])
                style_underline = '{{{0}}}text-underline-style'.format(namespaces['style'])
                style_position = '{{{0}}}text-position'.format(namespaces['style'])
                
                for attr_name in [fo_weight, fo_style, style_underline, style_position]:
                    if attr_name in text_prop.attrib:
                        style_properties[attr_name] = text_prop.attrib[attr_name]
            
            automatic_styles[style_name] = style_properties
        
        # Generate HTML
        html = []        
        # Process paragraphs
        for paragraph in root.findall('.//text:p', namespaces):
            p_style_name = paragraph.get('{{{0}}}style-name'.format(namespaces['text']))
            
            # Get paragraph style name
            p_style_name = paragraph.get('{{{0}}}style-name'.format(namespaces['text']))
            
            # Get fully resolved paragraph style
            p_style = {}
            if p_style_name:
                # Combine both style hierarchies for complete resolution
                combined_hierarchy = {**style_hierarchy, **auto_style_hierarchy}
                
                # Try resolving from automatic styles first
                if p_style_name in automatic_styles:
                    p_style = __resolve_style(p_style_name, automatic_styles, combined_hierarchy, styles)
                # Then try document styles
                elif p_style_name in styles:
                    p_style = __resolve_style(p_style_name, styles, combined_hierarchy, automatic_styles)
            
            # Extract paragraph formatting attributes
            text_align = 'left'  # Default
            p_is_bold = False
            p_is_italic = False
            p_is_underline = False
            p_is_superscript = False
            p_is_subscript = False
            
            # Get alignment
            fo_align = '{{{0}}}text-align'.format(namespaces['fo'])
            if fo_align in p_style:
                text_align = p_style[fo_align]
                
            # Get basic text formatting from paragraph style (for inheritance)
            fo_weight = '{{{0}}}font-weight'.format(namespaces['fo'])
            if fo_weight in p_style and p_style[fo_weight] == 'bold':
                p_is_bold = True
                
            fo_style = '{{{0}}}font-style'.format(namespaces['fo'])
            if fo_style in p_style and p_style[fo_style] == 'italic':
                p_is_italic = True
                
            style_text_underline = '{{{0}}}text-underline-style'.format(namespaces['style'])
            if style_text_underline in p_style and p_style[style_text_underline] != 'none':
                p_is_underline = True
                
            style_text_position = '{{{0}}}text-position'.format(namespaces['style'])
            if style_text_position in p_style:
                position = p_style[style_text_position]
                if position.startswith('super'):
                    p_is_superscript = True
                elif position.startswith('sub'):
                    p_is_subscript = True
            
            # Start paragraph with alignment
            html.append(f'<p class="odt_paragraphs" style="text-align: {text_align};">')
            
            # Process paragraph content
            # First, handle direct text content of the paragraph with paragraph's formatting
            if paragraph.text and paragraph.text.strip():
                text = paragraph.text
                
                # Apply paragraph formatting to direct text
                if p_is_subscript:
                    text = f'<sub>{text}</sub>'
                if p_is_superscript:
                    text = f'<sup>{text}</sup>'
                if p_is_underline:
                    text = f'<u>{text}</u>'
                if p_is_italic:
                    text = f'<i>{text}</i>'
                if p_is_bold:
                    text = f'<b>{text}</b>'
                    
                html.append(text)
            
            # Process all children
            for child in paragraph:
                if child.tag == '{{{0}}}span'.format(namespaces['text']):
                    span_style_name = child.get('{{{0}}}style-name'.format(namespaces['text']))
                    span_style = {}
                    
                    # Get span style
                    if span_style_name in automatic_styles:
                        span_style = automatic_styles[span_style_name]
                    elif span_style_name in styles:
                        span_style = styles[span_style_name]
                    
                    # Process text with formatting
                    text = child.text or ''
                    
                    # Inherit formatting from paragraph style if not defined in span style
                    is_bold = p_is_bold
                    is_italic = p_is_italic
                    is_underline = p_is_underline
                    is_superscript = p_is_superscript
                    is_subscript = p_is_subscript
                    
                    # Override with span-specific formatting if defined
                    # Bold
                    fo_weight = '{{{0}}}font-weight'.format(namespaces['fo'])
                    if fo_weight in span_style:
                        is_bold = span_style[fo_weight] == 'bold'
                    
                    # Italic
                    fo_style = '{{{0}}}font-style'.format(namespaces['fo'])
                    if fo_style in span_style:
                        is_italic = span_style[fo_style] == 'italic'
                    
                    # Underline
                    style_text_underline = '{{{0}}}text-underline-style'.format(namespaces['style'])
                    if style_text_underline in span_style:
                        is_underline = span_style[style_text_underline] != 'none'
                    
                    # Superscript/subscript
                    style_text_position = '{{{0}}}text-position'.format(namespaces['style'])
                    if style_text_position in span_style:
                        position = span_style[style_text_position]
                        is_superscript = position.startswith('super')
                        is_subscript = position.startswith('sub')
                    
                    # Apply formatting (order matters for nested tags)
                    if is_subscript:
                        text = f'<sub>{text}</sub>'
                    if is_superscript:
                        text = f'<sup>{text}</sup>'
                    if is_underline:
                        text = f'<u>{text}</u>'
                    if is_italic:
                        text = f'<i>{text}</i>'
                    if is_bold:
                        text = f'<b>{text}</b>'
                    
                    html.append(text)
                
                # Handle line breaks
                elif child.tag == '{{{0}}}line-break'.format(namespaces['text']):
                    html.append('<br/>')
                
                # Handle other elements (with paragraph formatting)
                elif child.text and child.text.strip():
                    text = child.text
                    
                    # Apply paragraph formatting
                    if p_is_subscript:
                        text = f'<sub>{text}</sub>'
                    if p_is_superscript:
                        text = f'<sup>{text}</sup>'
                    if p_is_underline:
                        text = f'<u>{text}</u>'
                    if p_is_italic:
                        text = f'<i>{text}</i>'
                    if p_is_bold:
                        text = f'<b>{text}</b>'
                        
                    html.append(text)
                
                # Handle tail text (text between spans) with paragraph formatting
                if child.tail and child.tail.strip():
                    text = child.tail
                    
                    # Apply paragraph formatting
                    if p_is_subscript:
                        text = f'<sub>{text}</sub>'
                    if p_is_superscript:
                        text = f'<sup>{text}</sup>'
                    if p_is_underline:
                        text = f'<u>{text}</u>'
                    if p_is_italic:
                        text = f'<i>{text}</i>'
                    if p_is_bold:
                        text = f'<b>{text}</b>'
                        
                    html.append(text)
            
            html.append('</p>')
    
    return ''.join(html)
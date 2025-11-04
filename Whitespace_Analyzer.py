#!/usr/bin/env python3
"""
Universal Whitespace Steganography Analyzer
Usage: python3 whitespace_analyzer.py <filename>
"""

import sys
import os
import argparse

def analyze_whitespace(filename):
    """Comprehensive whitespace steganography analysis"""
    
    if not os.path.exists(filename):
        print(f"❌ Error: File '{filename}' not found")
        return
    
    print(f"🔍 Analyzing: {filename}")
    print("=" * 50)
    
    with open(filename, 'rb') as f:
        raw_content = f.read()
    
    with open(filename, 'r') as f:
        text_content = f.read()
    
    # 1. Basic file info
    print(f"📊 File size: {len(raw_content)} bytes")
    print(f"📝 Readable chars: {len([c for c in text_content if c.isprintable()])}")
    
    # 2. Raw hex dump (first 100 bytes)
    print("\n🔢 Hex dump (first 100 bytes):")
    hex_str = ' '.join(f'{b:02x}' for b in raw_content[:100])
    print(hex_str)
    
    # 3. Visible whitespace analysis
    print("\n👁️ Visible whitespace (cat -A style):")
    visible = text_content.replace(' ', '␣').replace('\t', '→').replace('\n', '⏎\n')
    print(repr(visible))
    
    # 4. Character frequency
    print("\n📈 Character frequency:")
    chars = {'space': 0, 'tab': 0, 'lf': 0, 'cr': 0, 'other': 0}
    for char in text_content:
        if char == ' ': chars['space'] += 1
        elif char == '\t': chars['tab'] += 1
        elif char == '\n': chars['lf'] += 1
        elif char == '\r': chars['cr'] += 1
        else: chars['other'] += 1
    
    for char_type, count in chars.items():
        print(f"  {char_type}: {count}")
    
    # 5. Binary conversion attempts
    print("\n🔤 Binary decoding attempts:")
    
    # Method 1: Space=0, Tab=1
    binary1 = text_content.replace(' ', '0').replace('\t', '1').replace('\n', '')
    print(f"Space=0, Tab=1: {binary1[:80]}...")
    
    # Method 2: Tab=0, Space=1  
    binary2 = text_content.replace('\t', '0').replace(' ', '1').replace('\n', '')
    print(f"Tab=0, Space=1: {binary2[:80]}...")
    
    # 6. Try to extract ASCII from binary
    print("\n🔄 ASCII extraction:")
    
    def binary_to_ascii(binary_str, method_name):
        """Convert binary string to ASCII"""
        try:
            # Try 7-bit and 8-bit ASCII
            ascii_text = ""
            for i in range(0, len(binary_str)-6, 7):
                byte = binary_str[i:i+7]
                if len(byte) == 7:
                    decimal = int(byte, 2)
                    if 32 <= decimal <= 126:  # Printable ASCII
                        ascii_text += chr(decimal)
            return ascii_text if ascii_text else "No printable ASCII found"
        except:
            return "Conversion failed"
    
    result1 = binary_to_ascii(binary1, "Space=0, Tab=1")
    result2 = binary_to_ascii(binary2, "Tab=0, Space=1")
    
    print(f"Space=0, Tab=1: {result1}")
    print(f"Tab=0, Space=1: {result2}")
    
    # 7. Whitespace language detection
    print("\n🤖 Whitespace language analysis:")
    lines = text_content.split('\n')
    push_commands = [line for line in lines if line.startswith('   ')]
    print(f"Possible push commands: {len(push_commands)}")
    
    # 8. Stack simulation for Whitespace language
    if push_commands:
        print("Simulating stack operations:")
        stack = []
        for cmd in push_commands:
            # Remove push prefix and convert to binary
            num_part = cmd[3:]
            bin_num = num_part.replace(' ', '0').replace('\t', '1')
            if bin_num:
                try:
                    decimal = int(bin_num, 2)
                    stack.append(decimal)
                    if 32 <= decimal <= 126:
                        print(f"  Pushed: {decimal} -> ASCII: '{chr(decimal)}'")
                    else:
                        print(f"  Pushed: {decimal} (non-printable)")
                except:
                    print(f"  Could not parse: {repr(num_part)}")
        
        if stack:
            ascii_from_stack = ''.join(chr(x) for x in stack if 32 <= x <= 126)
            print(f"Extracted text: {ascii_from_stack}")

def main():
    parser = argparse.ArgumentParser(description='Whitespace Steganography Analyzer')
    parser.add_argument('filename', help='File to analyze')
    parser.add_argument('-v', '--verbose', action='store_true', help='Verbose output')
    
    args = parser.parse_args()
    
    if len(sys.argv) < 2:
        print("Usage: python3 whitespace_analyzer.py <filename>")
        sys.exit(1)
    
    analyze_whitespace(args.filename)

if __name__ == "__main__":
    main()

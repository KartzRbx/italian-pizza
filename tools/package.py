"""Build the declarative theme VSIX using only Python's standard library."""
import hashlib
import json
from pathlib import Path
import xml.etree.ElementTree as ET
import zipfile

ROOT = Path(__file__).resolve().parents[1]


def main():
    package = json.loads((ROOT / 'package.json').read_text(encoding='utf8'))
    namespace = 'http://schemas.microsoft.com/developer/vsx-schema/2011'
    ET.register_namespace('', namespace)
    manifest = ET.Element('PackageManifest', {'Version': '2.0.0', 'xmlns': namespace})
    metadata = ET.SubElement(manifest, 'Metadata')
    ET.SubElement(metadata, 'Identity', {'Language': 'en-US', 'Id': package['name'], 'Version': package['version'], 'Publisher': package['publisher']})
    ET.SubElement(metadata, 'DisplayName').text = package['displayName']
    ET.SubElement(metadata, 'Description', {'xml:space': 'preserve'}).text = package['description']
    ET.SubElement(metadata, 'Tags').text = ','.join(package['keywords'])
    ET.SubElement(metadata, 'Categories').text = 'Themes'
    ET.SubElement(metadata, 'GalleryFlags').text = 'Public'
    properties = ET.SubElement(metadata, 'Properties')
    for key, value in {'Microsoft.VisualStudio.Code.Engine': package['engines']['vscode'], 'Microsoft.VisualStudio.Code.ExtensionKind': 'ui', 'Microsoft.VisualStudio.Code.PreRelease': 'false', 'Microsoft.VisualStudio.Services.Links.Source': package['repository']['url'], 'Microsoft.VisualStudio.Services.Links.Getstarted': package['homepage']}.items():
        ET.SubElement(properties, 'Property', {'Id': key, 'Value': value})
    ET.SubElement(metadata, 'License').text = 'extension/LICENSE'
    ET.SubElement(metadata, 'Icon').text = 'extension/images/pizza.png'
    install = ET.SubElement(manifest, 'Installation')
    ET.SubElement(install, 'InstallationTarget', {'Id': 'Microsoft.VisualStudio.Code'})
    ET.SubElement(manifest, 'Dependencies')
    assets = ET.SubElement(manifest, 'Assets')
    for kind, path in [('Manifest', 'package.json'), ('Content.Details', 'README.md'), ('Content.License', 'LICENSE'), ('Icons.Default', 'images/pizza.png'), ('Content.Changelog', 'CHANGELOG.md')]:
        prefix = 'Microsoft.VisualStudio.Code.' if kind == 'Manifest' else 'Microsoft.VisualStudio.Services.'
        ET.SubElement(assets, 'Asset', {'Type': prefix + kind, 'Path': 'extension/' + path, 'Addressable': 'true'})
    content = ET.Element('Types', {'xmlns': 'http://schemas.openxmlformats.org/package/2006/content-types'})
    for extension, mime in {'json': 'application/json', 'md': 'text/markdown', 'png': 'image/png', 'svg': 'image/svg+xml', 'vsixmanifest': 'text/xml'}.items():
        ET.SubElement(content, 'Default', {'Extension': extension, 'ContentType': mime})
    files = ['package.json', 'README.md', 'CHANGELOG.md', 'LICENSE', 'palette.json', 'themes/italian-pizza-color-theme.json', 'images/pizza.png', 'images/pizza.svg', 'images/preview.png']
    for name in files:
        assert (ROOT / name).is_file(), name
    out = ROOT / 'dist' / f"{package['name']}-{package['version']}.vsix"
    out.parent.mkdir(exist_ok=True)
    with zipfile.ZipFile(out, 'w', zipfile.ZIP_DEFLATED) as archive:
        archive.writestr('extension.vsixmanifest', ET.tostring(manifest, encoding='utf8', xml_declaration=True))
        archive.writestr('[Content_Types].xml', ET.tostring(content, encoding='utf8', xml_declaration=True))
        for name in files:
            archive.write(ROOT / name, 'extension/' + name)
    checksum = hashlib.sha256(out.read_bytes()).hexdigest()
    (out.parent / 'SHA256SUMS').write_text(f'{checksum}  {out.name}\n', encoding='ascii')
    print(out)
    print(checksum)


if __name__ == '__main__':
    main()

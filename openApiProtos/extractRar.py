import rarfile

rar = rarfile.RarFile('/mnt/data/openapi.rar')
rar.extractall('./extracted')
print("✅ Extraction complete.")

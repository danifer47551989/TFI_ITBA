from pathlib import Path
import pandas as pd

# Raíz del proyecto TFI_ITBA
PROJECT_ROOT = Path(__file__).resolve().parent.parent

# Carpetas
input_dir = PROJECT_ROOT / "data" / "raw"
output_dir = PROJECT_ROOT / "data" / "parquet"

output_dir.mkdir(parents=True, exist_ok=True)

csv_files = list(input_dir.glob("*.csv"))

print(f"Proyecto: {PROJECT_ROOT}")
print(f"Buscando CSV en: {input_dir}")
print(f"Guardando Parquet en: {output_dir}")
print(f"CSV encontrados: {len(csv_files)}")
print()

if not csv_files:
    raise FileNotFoundError(
        f"No se encontraron archivos CSV en {input_dir}"
    )

for csv_file in csv_files:

    print("=" * 70)
    print(f"Procesando: {csv_file.name}")

    df = pd.read_csv(csv_file)

    output_file = output_dir / f"{csv_file.stem}.parquet"

    df.to_parquet(
        output_file,
        engine="pyarrow",
        compression="zstd",
        index=False
    )

    csv_size = csv_file.stat().st_size / (1024 ** 2)
    parquet_size = output_file.stat().st_size / (1024 ** 2)

    reduction = (1 - parquet_size / csv_size) * 100

    print(f"Filas:       {len(df):,}")
    print(f"CSV:         {csv_size:.2f} MB")
    print(f"Parquet:     {parquet_size:.2f} MB")
    print(f"Reducción:   {reduction:.1f}%")
    print(f"Generado:    {output_file.name}")

print()
print("=" * 70)
print(f"Conversión terminada: {len(csv_files)} archivos.")
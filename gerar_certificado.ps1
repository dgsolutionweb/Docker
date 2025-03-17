# Script para gerar certificado SSL autoassinado
# Para uso em ambiente de testes/desenvolvimento
# Em produção, use Let's Encrypt ou um certificado válido

# Configurações do certificado
$dominio = "localhost" # Substitua pelo seu domínio
$certificadoDir = ".\nginx\ssl"
$certificadoCrt = "$certificadoDir\estoque.crt" 
$certificadoKey = "$certificadoDir\estoque.key"

# Criar diretório se não existir
if (!(Test-Path $certificadoDir)) {
    New-Item -ItemType Directory -Path $certificadoDir -Force
}

# Comandos do OpenSSL para gerar certificado
# Nota: Você precisa ter o OpenSSL instalado no seu sistema
# Caso contrário, pode baixar em: https://slproweb.com/products/Win32OpenSSL.html

# Gere sua chave privada
Write-Host "Gerando chave privada..."
openssl genrsa -out $certificadoKey 2048

# Gere um CSR (Certificate Signing Request)
Write-Host "Gerando CSR..."
openssl req -new -key $certificadoKey -out "$certificadoDir\estoque.csr" -subj "/C=BR/ST=Estado/L=Cidade/O=SuaEmpresa/OU=TI/CN=$dominio"

# Gere o certificado autoassinado
Write-Host "Gerando certificado autoassinado..."
openssl x509 -req -days 365 -in "$certificadoDir\estoque.csr" -signkey $certificadoKey -out $certificadoCrt

Write-Host "Certificado gerado com sucesso!" 
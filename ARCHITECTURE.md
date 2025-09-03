# Arquitetura do AurantisSync

## Visão Geral

O AurantisSync é um aplicativo de desktop modular construído com Python e PySide6, seguindo uma arquitetura em camadas bem definida.

## Estrutura de Camadas

```
┌─────────────────────────────────────────┐
│              UI Layer                   │
│  (PySide6 - Interface do Usuário)      │
├─────────────────────────────────────────┤
│            Widgets Layer                │
│  (Componentes Customizados)            │
├─────────────────────────────────────────┤
│             Core Layer                  │
│  (Lógica de Negócio)                   │
├─────────────────────────────────────────┤
│           External Layer                │
│  (Bibliotecas Externas)                │
└─────────────────────────────────────────┘
```

## Componentes Principais

### 1. UI Layer (`app/ui/`)
- **main_window.py**: Janela principal com layout e navegação
- Responsável por coordenar todos os widgets
- Gerencia eventos de menu e atalhos de teclado
- Controla o fluxo principal da aplicação

### 2. Widgets Layer (`app/widgets/`)
- **waveform_widget.py**: Visualização de waveform com controles de áudio
- **lines_table.py**: Tabela para edição de linhas de letra
- Widgets customizados que encapsulam funcionalidades específicas
- Comunicação com a camada core através de sinais

### 3. Core Layer (`app/core/`)

#### sync_model.py
- **SyncProject**: Classe principal do projeto
- **LyricLine**: Modelo de dados para linhas de letra
- Operações de manipulação de linhas (dividir, unir, normalizar)

#### transcriber.py
- **Transcriber**: Interface com faster-whisper
- Detecção de FFmpeg
- Conversão de formatos de áudio
- Gerenciamento de modelos do Whisper

#### audio_player.py
- **AudioPlayer**: Reprodução de áudio com controles avançados
- Suporte a velocidade variável
- Controle de volume
- Callbacks para sincronização com UI

#### waveform.py
- **WaveformGenerator**: Geração e análise de waveform
- Detecção de silêncio
- Análise espectral
- Redimensionamento de dados

#### exporters.py
- **Exporter**: Exportação para múltiplos formatos
- Suporte a TXT, SRT, LRC, VTT, JSON
- Validação de dados
- Tratamento de erros

#### project_io.py
- **ProjectIO**: Sistema de persistência
- Salvamento/carregamento de projetos
- Sistema de autosave
- Gerenciamento de versões

## Fluxo de Dados

### 1. Carregamento de Áudio
```
Arquivo de Áudio → AudioPlayer → WaveformGenerator → WaveformWidget
```

### 2. Transcrição
```
Arquivo de Áudio → Transcriber → Lista de LyricLine → LinesTableWidget
```

### 3. Edição
```
LinesTableWidget ↔ SyncProject ↔ WaveformWidget
```

### 4. Exportação
```
SyncProject → Exporter → Arquivos de Saída
```

## Padrões de Design Utilizados

### 1. Model-View-Controller (MVC)
- **Model**: SyncProject, LyricLine
- **View**: WaveformWidget, LinesTableWidget
- **Controller**: MainWindow

### 2. Observer Pattern
- Sinais PySide6 para comunicação entre componentes
- Callbacks para eventos de áudio
- Sistema de notificações de mudanças

### 3. Factory Pattern
- Exporter para diferentes formatos de saída
- Criação de widgets customizados

### 4. Singleton Pattern
- Transcriber (modelo carregado uma vez)
- AudioPlayer (instância única)

## Threading e Concorrência

### 1. Transcrição em Background
- TranscriptionThread para operações longas
- UI responsiva durante processamento
- Sinais para atualização de progresso

### 2. Reprodução de Áudio
- Threading interno do sounddevice
- Callbacks thread-safe
- Sincronização com UI

### 3. Autosave
- Timer para salvamento automático
- Operações não-bloqueantes

## Gerenciamento de Estado

### 1. Estado Global
- SyncProject: estado principal da aplicação
- AudioPlayer: estado de reprodução
- Transcriber: estado do modelo carregado

### 2. Estado Local
- Widgets mantêm estado de UI
- Sincronização através de sinais

### 3. Persistência
- Projetos salvos em JSON
- Autosave em intervalos regulares
- Recuperação de projetos corrompidos

## Tratamento de Erros

### 1. Validação de Entrada
- Verificação de formatos de arquivo
- Validação de timestamps
- Verificação de dependências

### 2. Recuperação de Erros
- Fallback para CPU se GPU não disponível
- Conversão automática de formatos
- Recuperação de autosave

### 3. Feedback ao Usuário
- Mensagens de erro claras
- Logs de status
- Indicadores de progresso

## Extensibilidade

### 1. Novos Formatos de Exportação
- Implementar função de exportação
- Adicionar ao dicionário FORMATS
- Interface automática

### 2. Novos Modelos de Transcrição
- Extensão da classe Transcriber
- Configuração de parâmetros
- Interface unificada

### 3. Novos Widgets
- Herança de QWidget
- Integração com sistema de sinais
- Documentação de API

## Performance

### 1. Otimizações de Memória
- Carregamento lazy de modelos
- Limpeza de dados temporários
- Gerenciamento de cache

### 2. Otimizações de CPU
- Processamento em background
- Uso de GPU quando disponível
- Algoritmos eficientes

### 3. Otimizações de I/O
- Operações assíncronas
- Cache de arquivos
- Compressão de dados

## Segurança

### 1. Validação de Arquivos
- Verificação de tipos MIME
- Sanitização de caminhos
- Limitação de tamanho

### 2. Isolamento de Processos
- Threading seguro
- Gerenciamento de recursos
- Cleanup automático

## Testabilidade

### 1. Separação de Responsabilidades
- Módulos independentes
- Interfaces bem definidas
- Baixo acoplamento

### 2. Injeção de Dependências
- Mocks para testes
- Configuração flexível
- Isolamento de componentes

### 3. Testes Automatizados
- Script de teste integrado
- Verificação de dependências
- Validação de funcionalidades

# AI

1. Prompt engineering
2. Retrieval Augmented Generation (RAG)
3. Agents / Multi modal / Model Context Protocol (MCP) / Harness / Skills
4. Finetuning / training small language or open weight models


lemmatization
- Tokens 
- Parameters 
- Context windows

### Models

- Proprietary 
    + Chat GPT 
    + Claude 
    + Gemini 
    + Grok 
    + Suno
    + Llama 
- Open weight / Free to use models
    + Industry / US
        - Google - Gemma
        - OpenAI - GPT-OSS
        - Meta - Llama 
    + Industry / China 
        - Deepseek 
        - Kimi
        - Qwen
        - MiniMax


### Tools
- To host - ollama.com
- Harnes - pi.dev


##### To see models
```bash
ollma ls
```

##### To load a model
```bash
ollma run model-name:size
```

##### To launch a harness
```bash
ollma launch harnes --model model-name:size
```

##### To launch a pi with kimi-k2.6:cloud
```bash
ollma launch pi --model kimi-k2.6:cloud
```

- To get out of ollama CTRL+D 
- To get oit of a harnes CTRL+C twice

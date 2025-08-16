// List of model profiles (presets)
export const MODEL_PROFILES = [
  {
    name: "Ultra Fast",
    description: "Low temperature, max tokens 256, fast responses.",
    params: { model: "Llama-3.3-8B-Instruct", temperature: 0.2, max_tokens: 256 }
  },
  {
    name: "Balanced",
    description: "Default settings for general chat.",
    params: { model: "Llama-3.3-8B-Instruct", temperature: 0.7, max_tokens: 512 }
  },
  {
    name: "Creative Genius",
    description: "High temperature, longer responses, creative output.",
    params: { model: "Llama-3.3-8B-Instruct", temperature: 1.2, max_tokens: 1024 }
  },
  {
    name: "Ultra Long Context",
    description: "Lower temperature, max tokens 2048, for long-form answers.",
    params: { model: "Llama-3.3-8B-Instruct", temperature: 0.5, max_tokens: 2048 }
  }
];

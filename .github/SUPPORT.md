# Support

## Getting Help

If you need help with AurantisSync, here are the best ways to get support:

### 📚 Documentation

1. **README.md** - Start here for basic information
2. **QUICKSTART.md** - Quick setup guide
3. **CHANGELOG.md** - Version history and updates

### 🐛 Bug Reports

If you found a bug:

1. Check if it's already reported in [Issues](https://github.com/JoaoSantosCodes/AurantisSync/issues)
2. If not, create a new issue using the [Bug Report template](https://github.com/JoaoSantosCodes/AurantisSync/issues/new?template=bug_report.md)
3. Include:
   - Your operating system
   - Python version
   - FFmpeg version
   - Steps to reproduce
   - Error messages (if any)

### 💡 Feature Requests

Have an idea for a new feature?

1. Check if it's already requested in [Issues](https://github.com/JoaoSantosCodes/AurantisSync/issues)
2. If not, create a new issue using the [Feature Request template](https://github.com/JoaoSantosCodes/AurantisSync/issues/new?template=feature_request.md)
3. Describe:
   - What you want to achieve
   - Why it would be useful
   - How it should work

### ❓ Questions

For general questions:

1. Check the [FAQ](#faq) below
2. Search existing [Issues](https://github.com/JoaoSantosCodes/AurantisSync/issues) and [Discussions](https://github.com/JoaoSantosCodes/AurantisSync/discussions)
3. Create a new [Discussion](https://github.com/JoaoSantosCodes/AurantisSync/discussions) if your question isn't answered

### 🔧 Troubleshooting

#### Common Issues

**FFmpeg not found**
- Windows: Add `C:\ffmpeg\bin` to your PATH
- macOS: `brew install ffmpeg`
- Linux: `sudo apt install ffmpeg`

**Dependencies not installing**
```bash
pip install --upgrade pip
pip install -r requirements.txt
```

**App not starting**
```bash
python test_mvp.py
```

**Transcription errors**
- Check if your audio file is supported
- Try a different Whisper model
- Ensure FFmpeg is working: `ffmpeg -version`

#### Getting System Information

Run this to get system info for bug reports:

```bash
python -c "
import sys, platform
print(f'Python: {sys.version}')
print(f'OS: {platform.system()} {platform.release()}')
print(f'Architecture: {platform.machine()}')
"
```

### 📞 Contact

- **GitHub Issues**: [Create an issue](https://github.com/JoaoSantosCodes/AurantisSync/issues)
- **GitHub Discussions**: [Start a discussion](https://github.com/JoaoSantosCodes/AurantisSync/discussions)
- **Email**: [your-email@example.com]

### 🤝 Contributing

Want to contribute? Great! Check out our [Contributing Guidelines](CONTRIBUTING.md).

### 📄 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## FAQ

### Q: What audio formats are supported?
A: WAV, MP3, M4A, FLAC, OGG, AAC

### Q: What languages are supported for transcription?
A: Portuguese, English, Spanish, French, German, Italian, Japanese, Korean, Chinese

### Q: Can I use GPU for faster transcription?
A: Yes, if you have CUDA installed, the app will automatically use GPU

### Q: How accurate is the transcription?
A: It depends on the audio quality and language. The "large-v3" model is most accurate but slower

### Q: Can I edit the transcribed text?
A: Yes, you can edit both the text and timestamps in the table

### Q: What export formats are available?
A: TXT, SRT, LRC, VTT, and JSON

### Q: Is my audio data sent to external servers?
A: No, all processing is done locally on your machine

### Q: Can I build an executable?
A: Yes, use `python build_advanced.py` or `build_exe.bat`

### Q: How do I update the app?
A: Download the latest version from GitHub and replace the files

### Q: Can I use this commercially?
A: Yes, the MIT license allows commercial use

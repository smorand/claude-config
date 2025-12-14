# Supported Language Codes

## Common Languages

| Language | Code |
|----------|------|
| French | `fr` |
| Spanish | `es` |
| German | `de` |
| Italian | `it` |
| Portuguese | `pt` |
| Japanese | `ja` |
| Chinese (Simplified) | `zh` |
| Korean | `ko` |
| Arabic | `ar` |
| Russian | `ru` |
| Dutch | `nl` |
| Polish | `pl` |
| Turkish | `tr` |
| Swedish | `sv` |
| Norwegian | `no` |
| Danish | `da` |
| Finnish | `fi` |
| Greek | `el` |
| Hebrew | `he` |
| Hindi | `hi` |

## European Languages

| Language | Code |
|----------|------|
| Bulgarian | `bg` |
| Croatian | `hr` |
| Czech | `cs` |
| Estonian | `et` |
| Hungarian | `hu` |
| Irish | `ga` |
| Latvian | `lv` |
| Lithuanian | `lt` |
| Maltese | `mt` |
| Romanian | `ro` |
| Slovak | `sk` |
| Slovenian | `sl` |
| Ukrainian | `uk` |

## Asian Languages

| Language | Code |
|----------|------|
| Bengali | `bn` |
| Chinese (Traditional) | `zh-TW` |
| Filipino | `fil` |
| Indonesian | `id` |
| Javanese | `jv` |
| Khmer | `km` |
| Lao | `lo` |
| Malay | `ms` |
| Marathi | `mr` |
| Nepali | `ne` |
| Punjabi | `pa` |
| Sinhala | `si` |
| Tamil | `ta` |
| Telugu | `te` |
| Thai | `th` |
| Urdu | `ur` |
| Vietnamese | `vi` |

## Other Languages

| Language | Code |
|----------|------|
| Afrikaans | `af` |
| Albanian | `sq` |
| Amharic | `am` |
| Armenian | `hy` |
| Azerbaijani | `az` |
| Basque | `eu` |
| Belarusian | `be` |
| Bosnian | `bs` |
| Catalan | `ca` |
| Cebuano | `ceb` |
| Corsican | `co` |
| Esperanto | `eo` |
| Frisian | `fy` |
| Galician | `gl` |
| Georgian | `ka` |
| Gujarati | `gu` |
| Haitian Creole | `ht` |
| Hausa | `ha` |
| Hawaiian | `haw` |
| Hmong | `hmn` |
| Icelandic | `is` |
| Igbo | `ig` |
| Kannada | `kn` |
| Kazakh | `kk` |
| Kurdish | `ku` |
| Kyrgyz | `ky` |
| Latin | `la` |
| Luxembourgish | `lb` |
| Macedonian | `mk` |
| Malagasy | `mg` |
| Malayalam | `ml` |
| Maori | `mi` |
| Mongolian | `mn` |
| Myanmar (Burmese) | `my` |
| Nyanja (Chichewa) | `ny` |
| Odia (Oriya) | `or` |
| Pashto | `ps` |
| Persian | `fa` |
| Samoan | `sm` |
| Scots Gaelic | `gd` |
| Serbian | `sr` |
| Sesotho | `st` |
| Shona | `sn` |
| Sindhi | `sd` |
| Somali | `so` |
| Sundanese | `su` |
| Swahili | `sw` |
| Tajik | `tg` |
| Uzbek | `uz` |
| Welsh | `cy` |
| Xhosa | `xh` |
| Yiddish | `yi` |
| Yoruba | `yo` |
| Zulu | `zu` |

## Regional Variants

Some languages have regional variants:

| Language | Code | Region |
|----------|------|--------|
| Portuguese (Brazil) | `pt-BR` | Brazil |
| Portuguese (Portugal) | `pt-PT` | Portugal |
| Spanish (Latin America) | `es-419` | Latin America |
| English (UK) | `en-GB` | United Kingdom |
| English (US) | `en-US` | United States |

## Notes

- All codes are ISO 639-1 two-letter codes
- Some regional variants use ISO 639-1 plus region code
- Auto-detection works for all supported source languages
- 100+ languages supported by Google Cloud Translation API
- For unlisted languages, try the 2-letter ISO code

## Usage

```bash
# Use 2-letter code as third argument
~/.claude/skills/google-slides-translator/scripts/run.sh translate_slides <id> <range> <code>

# Examples
~/.claude/skills/google-slides-translator/scripts/run.sh translate_slides 1abc123 all fr    # French
~/.claude/skills/google-slides-translator/scripts/run.sh translate_slides 1abc123 all ja    # Japanese
~/.claude/skills/google-slides-translator/scripts/run.sh translate_slides 1abc123 all zh    # Chinese
~/.claude/skills/google-slides-translator/scripts/run.sh translate_slides 1abc123 all pt-BR # Portuguese (Brazil)
```

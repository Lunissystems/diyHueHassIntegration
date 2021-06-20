# DIY Hue Integration

### Installation

Copy this folder to `<config_dir>/custom_components/example_light/`.

Add the following entry in your `configuration.yaml`:

```yaml
light:
  - platform: awesome_lights
    host: HOST_HERE
    username: USERNAME_HERE
    password: PASSWORD_HERE_OR_secrets.yaml
```

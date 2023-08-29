## v1.2.0

- Bump minimum NetBox version to v3.4
- Update author to NetBox Labs
- Replace navigation menu hack with proper PluginMenu implementation (#2)
- Fix ValueError exception when loading reports (#3)

## v1.1.0

- Added SAML XML export API Endpoint saml.xml
- Fixed config api to only send strings as values
- Remove native database backup functionality (replaced by portal)

## v1.0.0

- Populate initial data for configuration form from global settings (#10)

## v0.2.2

- Automatically run database migrations when config is updated (#6)

## v0.2.1

- Add support for netbox-secretstore plugin
- Fix database export (#13)

## v0.2.0

- Require NetBox v3.2
- Add support for administering plugins
- Add SSO configuration for Microsoft Azure AD, Okta OIDC

## v0.1.0

- Initial release

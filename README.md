# nexy-storage

File uploads and storage for Nexy apps: one API for the local disk and the object stores, with
signed URLs and image variants.

## What it covers

| Area | First version |
|---|---|
| Uploads | multipart and direct-to-bucket uploads, size and type limits, progress on the client |
| Backends | local disk in development, Amazon S3, Cloudflare R2, any S3-compatible store |
| Access | public files, private files behind signed URLs with an expiry |
| Images | resized and converted variants (WebP, AVIF), made on upload or on first request |
| Integration | works with the `Image` component and with Nexy forms and actions |

## Branches and releases

`develop` is the integration branch. Work branches start from `develop` and target `develop`.
`main` receives reviewed merges and release commits. The release workflow is prepared but dormant
until this module has a package to publish. See `docs/release-setup.md` for the registry setup.

## Status

Design phase. Nothing is published yet.

## License

MIT

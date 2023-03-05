# GnuPG Authorizer
Authorizer based on GnuPG `clearsign` signatures. Downloads the public keys from an endpoint that serves them as asc-files.

## Environment Configuration

| Env name       | Default | Description                                                             |
|----------------|:-------:|-------------------------------------------------------------------------|
| GRACE_PERIOD   |   60    | Grace period or timeout of a GnuPG signature in seconds                 |
| GPG_HOME       | `/tmp/` | GnuPG home folder which either contains, or will contain GnuPG keyrings |
| GPG_BIN        |  `gpg`  | Path (or command) to GnuPG binary                                       |
| PUBLIC_KEY_URL |         | URL to internet endpoint that serves public keys as asc-file            |

## Application flow
```mermaid
flowchart 
    cold[Cold start]
    retrieve[Retrieve Public Keys from URL]
    prepare[Prepare GnuPG environment]
    wait[Wait for request]
    decode[Decode signature form base64]
    verify[Verify signature]
    respond[Return validation]

    cold --> retrieve --> prepare --> wait
    wait --> decode --> verify --> respond
    respond --> wait

```
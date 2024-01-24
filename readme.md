# Introduction 

PROCESS-STREAM-MEDIA is a homage to [WatchVideoByLink](https://github.com/MohamedBakoush/WatchVideoByLink), aiming to improve my creation from scratch, developing something I can track and maintain until I lose interest.

## STILL PROTOTYPING ... THINGS MAY CHANGE

<kbd><img src="./assets/TOP-LEVEL-ARCHITECTURE.png" title="TOP LEVEL ARCHITECTURE"/></kbd> 

CLIENT SERVER:
- UPLOAD VIDEO 
- SELECT UPLOADED VIDEO
- WATCH UPLOADED VIDEO
- CUSTOM VIDEO PLAYER
- PRISMA (CONNECT TO PSQL DATABASE)

STREAM SERVER:
- PYTHON FLASK PROXY 
- NGINX VIDEO/IMAGE MEDIA STREAM 

UPLOAD SERVER:
- DOWNLOAD UPLOADED VIDEO
- RE-ENCODE VIDEO + DELETE UPLOADED VIDEO
- GENERATE THUMBNAILS 

SUPABASE DATABASE: 
- USER AUTHENTICATION 

PSQL DATABASE:
- INFO
- VIDEOS
- THUMBNAILS

## Before Start
In `.env`, replace `SUPABASE_KEY="xxx"` with anon key provided by supabase. https://supabase.com/docs/guides/cli/local-development
 
## Start Containers 

```
supabase start
docker-compose up --build
```

## Stop Containers

```
supabase stop 
docker-compose down 
```

## Stop Containers + Delete Volumes

```
supabase stop --no-backup
docker-compose down -v   
```

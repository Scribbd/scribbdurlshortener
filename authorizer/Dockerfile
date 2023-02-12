FROM public.ecr.aws/docker/library/python:3.9-slim as build

WORKDIR /app

RUN apt-get update && \
    apt-get install gcc -y

COPY requirements.txt .

RUN python3 -m pip install -r requirements.txt -t .


FROM public.ecr.aws/lambda/python:3.9

COPY /src .
COPY --from=build /app/ .


CMD ["src.gnupg.lambda_handler"]
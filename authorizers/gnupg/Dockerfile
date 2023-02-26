FROM public.ecr.aws/docker/library/python:3.9-slim as build
WORKDIR /app
COPY requirements.txt .
RUN python3 -m pip install -r requirements.txt -t .

FROM public.ecr.aws/lambda/python:3.9 as gnupg
RUN yum install git tar gcc make bzip2 hostname -y
RUN git clone https://github.com/skeeto/lean-static-gpg.git .
RUN ./build.sh

FROM public.ecr.aws/lambda/python:3.9
COPY --from=gnupg ${LAMBDA_TASK_ROOT}/gnupg ${LAMBDA_TASK_ROOT}
COPY --from=build /app/ ${LAMBDA_TASK_ROOT}
COPY /src ${LAMBDA_TASK_ROOT}
CMD ["src.authorizer.lambda_handler"]
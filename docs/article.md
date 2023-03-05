# The private URL shortener project

That includes a way to add/remove redirects without the need of directly manipulating the slug-database.

## Why this project

My inspiration came from a [blog](https://technology.amis.nl/aws/personal-link-shortener-in-aws/). That the author is also my wonderful colleague helped with getting this ball rolling. 

However, instead of just copying someone else's homework, I wish to improve upon it. The solution detailed in the blog requires direct manipulation of the underlying database to update redirects. I wished to put that also behind the API I am creating. Spoiler warning, due to my stubbornness, security took the most time to implement.

## Choices made

A short overview of deliberate choices made starting and during this project.

### SAM

In a former job, I was an [AWS re/Start](https://aws.amazon.com/training/restart/) instructor. In that job, I always had to tell how [SAM](https://aws.amazon.com/serverless/sam/) provdes 'shorthand syntax that offers high-level constructs and easy tooling for creating and testing serverless applications'. The sentence is actually longer, but you get the gist: I had to sell it to my participants. However, I never used it. I thought this would be a good project to actually get experience with this framework. 

My evaluation: It is a good framework. SAM made it way easier for me to deploy this application compared to writing it in pure [CloudFormation](https://aws.amazon.com/cloudformation/). It isn't as powerful as [CDK](https://aws.amazon.com/cdk/), but SAM has the advantage that you don't need to learn how to write CDK if you already know how to write CloudFormation. For the specific usecase SAM is made for, it really made the CloudFormation more streamlined and less verbose. Yet, I don't see me using it much. Even in this small project, I was hitting the walls of this framework and I will probably choose CDK in version 2 of this project.

### HTTP API Gateway (GatewayV2)

A side-grade from the original implementation that used the REST API gateway. Funny thing, when looking through the CloudFormation specification, I originally thought I had 4 options. HTTP and Rest on V1 and again on V2 of the API Gateway. Color me surprised when I found out that REST is actually the [ApiGateway(V1)](https://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/AWS_ApiGateway.html), and HTTP is the [ApiGatewayV2](https://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/AWS_ApiGatewayV2.html). The choice for the HTTP ApiGateway was made purely for monetary reasons.

I don't have a verdict on the Gateways. I have never used the REST API Gateway; thus I am unable to compare. I only wish AWS didn't name them this ambiguously as Gateway and GatewayV2.
### GnuPG

[Gnu Privacy Guard](https://gnupg.org/)... If you read the spoiler a few paragraphs above, you might have realized why security took the most time for me to implement. A good secure implementation requires time. But there is a difference between taking time to think out a good secure application, and making it hard on yourself.

The choice was made as I was looking for a way to implement a custom lambda authorizer that does not require me to run additional servers or services. And I wanted to wedge my [YubiKey](https://www.yubico.com/products/yubikey-5-overview/) into it somehow. Furthermore, from all the protocols YubiKey supports, I chose to use the [Open PGP](https://www.openpgp.org/) key option as I was most familiar with it. I was already using it for signing my commits and encrypting my passwords, how hard would this be?

Very, and I will explain this in my [troubles section](#encountered-troubles) further down.
## Experimental side effects

Another short overview detailing fun side effects, not deliberate choices, made during the project.
### Lambda Powertools

I heard of [Lambda Powertools](https://awslabs.github.io/aws-lambda-powertools-python/2.9.1/), but I never had a reason to actually use it. Looking at the documentation, it is fit for implementing lambda functions for an API gateway. This also had the side effect of using [x-ray](https://aws.amazon.com/xray/) for the first time.

My verdict: an excellent addition to any project. Setting up tracing, logging, routing has been quick. And it is available as a Lambda Layer, so it is easy to include. I will probably be using it in all future Lambda functions.
### Finch

[Finch](https://github.com/runfinch/finch) is a new open-source project by AWS for developing containers. It is basically AWS-flavored podman. It is a nice tool made for macOS. And my short exploration of it was pleasant. Unfortunately, SAM does [not support finch](https://github.com/aws/aws-sam-cli/issues/4584). 

My verdict: it is fine. It does what it does on the tin. The only shame is that it does not integrate with SAM that well.
### OpenAPI

[OpenAPI](https://swagger.io/specification/v3/) is a way of documenting and developing(?) APIs. My first attempt was to build the API from this document. However, to actually have it import properly I also had to write it with the [AWS extension for OpenAPI](https://docs.aws.amazon.com/apigateway/latest/developerguide/api-gateway-swagger-extensions.html), which made it even more daunting. Instead, I made an export and amended my documentation to that.

My verdict: it was a great tool to plan out my API. I used a visual editor [Stoplight](https://stoplight.io/) to just click something together and went that as a base.
## Encountered Troubles

### SAM gen mishaps

SAM probably does not expect an authorizer to be defined inside the same project as an application. I manually had to add (read: [write base CloudFormation](https://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-lambda-permission.html)) the resource policy for it to function. Not a big deal, but was just a surprise when I encountered internal server errors without any useful logging.

I also had a weird moment when it generated two API Gateways with broken configurations. This was quickly resolved by renaming the  logical name of the API resource from `HttpApi` to something else. I suspect SAM got confused with the `AWS::Serverless::HttpApi` resource type, and did some wonky stuff with that? Maybe?
### The Journey of Authorizers

An expert told me once, in a course about CyberSecurity, that it is unwise to implement your own security and to go with standards. I didn't listen, and understand a little more what he meant.

My journey with my authorizer is long, so I split it off into its own document, [here](./AuthorizingHeadache.md).
## Next steps

I will be looking at other ways to authorize. I want to experiment with a few methods: I mentioned them at the start of this article. A flavor of JWT is a big candidate as I have plans for creating more personal API's.

Other fun extensions to this project might be to implement change logging and usage statistics.

New projects would be to implement a serverless JWT solution.

All things considered, I am just starting and there is still enough to do.

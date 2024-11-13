***Soru:*** Welcome back and the last video we spoke a lot about convolutional know networks, so on this video,

how about we answer the question, what is a convolutional neural network or Brackett's CNN.

So if you hear me say CNN again, is this just a reminder?

I'm probably referring to Convolutional Noor network rather than the news site.

So let's go through this line again when we first look at it is going to be very daunting.

Don't worry, we're going to step through this.

Let's have a look at the typical architecture of a CNN.

This is what we're working towards building.

So we start off, we got here the CNN model, he goes to aftercare as model sequential.

We've seen that before.

Now, what we haven't seen before is a bunch of these layers and probably their internal parameters.

So let's start to step through them.

We might have an input layer, which in our case is two Karas layers com d, which stands for Convolutional

Tudy, which for two dimensional data such as images that have height and width, that's that's where

the 2D comes from there.

Now, this has a bunch of parameters, filters, kernel size, activation input.

CHAIB We're going to step through them too much for now because we're going to we're going to go through

these as we get hands on with coding.

But this is an actual convolutional neural network.

So let's have a look.

What does it do?

The input layer takes in target images and preprocessor them for further layers, such as the typical

values.

The input shape might be the batch size, image, height, image, width and color channel.

So that's this variable here, the input shape.

And again, the input images are target images you'd like to discover patterns in and of course, the

typical values here can be whatever you can take a photo or video, because the video is just a series

of photos played over and over again of.

And we might have a convolution layer, actually the same here to come today.

We've got another one here to give carers come to day and it's got the same parameters as above.

It just it's missing this input shape parameter, but we've got the same values, 10 three in order.

Again, don't worry too much about what's happening internally here.

We're going to write lots of these and get used to them.

I just want you to get an overview of what an architecture of a CNN looks like.

Now, what does this CNN or the convolutional like do this layer extracts learns the most important

features from the target images?

And look, I've got a typo only to fix it.

What are the typical values?

Multiple.

You can create it with two layers, convex dx where X can be multiple values.

So we've got.

Com 2d here because we're working with images.

But as you'll see in later on modules, we can also use conv one day for text data and then there's

also.

Com three day for three dimensional data.

Then again, we'll go again, we've got the hidden activation, we've seen that before, so this is

a nonlinear activation function.

In our case, it's typically RELU for convolutional is what does it do?

It adds non-linearity to learn features.

We had a look in the previous module of what non-linearity is known straight lines, because remember,

a lot of the data in the world is is not just straight lines.

We need some curved lines to to help us figure out patterns or better yet, help our neural networks

figure out patterns.

Then we typically have a pooling layer of some sort in our cases to carers as Max Paul Tudi, you might

have guessed that today is the same we've got to do here, the same reason we've got to date, because

we're dealing with images which are hot by with two dimensional and then we've got pool size, too,

padding valid.

Not sure what those are just yet.

Again, we're going to go through those.

What does this do?

Reduces the dimensionality of learned image features.

Hmm.

So as we'll see later on, Max, Pawling, the layout, the pooling layer, if our convolutional layers

learn features from images such as if we're thinking about a car, a feature of a car might be the fact

that the hood is a straight line and the wheels are circular.

Those might be two features.

Again, we don't define these.

They are learned automatically by the convolutional layers.

So it might learn the most important features from a target image.

Then the pulling layer further reduces, so the pulling layer learns even the most important features

out of the already learned features.

So this layer dramatically reduces the number of calculations of a CNN has to say.

This is what I'm saying.

I'm probably going to say ICANN more than I am going to say convolutional neural network, because convolutional

neural network is a bit of a mouthful.

So the polling layer reduces the number of calculations ICANN has to make.

So that's what makes it really computationally efficient.

Then we have a fully connected layer, which is often the output layer.

Now we've seen this one before, T.F. Kharas layers dense and the output shape here is one you might

deduce from that that we're working with a binary classification problem.

We've also got the sigmoid activation function here.

Which is our output activation, again, this adds nonlinearities to the output layer.

Who we've been through a fair bit here, but you can go back through this on your own time, as I said,

we're going to go through this and have a lot of hands on experience writing, because I just wanted

to show you right at the start what we're working towards building.

And now to make this example concrete, this network here, this convolutional neural network, which

is actually the same as Tiny VTG, which is from the CNN Explainer website, will have a look at that

in a future video.

But if you want to jump ahead, you can also go to this website here.

This convolutional road network will actually work to build a computer vision algorithm to deduce whether

these photos are of pizza or a steak.

So we'll see how to build that later on, but finally.

Oh, got a little note here, a reminder, there are almost unlimited amount of ways you could stack

together a convolutional neural network.

This slide only demonstrates one.

Yeah, that's an important point.

All of these layers here, this is an architecture called Tiny VTG.

Again, the details will jump into that later on.

But a convolutional network is typically a stack of convolutional layers and pooling layers and a bunch

of nonlinear activations.

So let's have a look at it in terms of the colored block edition, this might be a simple CNN might

have some inputs which are images.

We might process those images.

In other words, turn them into tenses, split them into different colored channels, tend to flow,

will help us do this.

And then we pass it to our this is our architecture here, which is typically some sort of combination

of convolutional layers and usually relleno activation and pooling layers.

This could be just one of these or it could be ten of these.

And then finally, we top it off with a fully connected output layer.

And in this case, it's got the prediction correct.

We want it to predict pizza and it's done it.

Then we might go to a deeper CNN, which is again, that's where the deep and deep learning comes from,

is when you stack these layers on top of each other.

Our input images preprocessing as normal have a convolutional layer, appalling layer upon layer upon

layer upon layer upon layer.

That could be a song conveyor pulling out.

I'll stop.

And then again, a fully connected output layer.

So we've seen enough.

We've seen enough pictures.

We've seen enough slides.

Let's code.

I'll see you in the next video, we're going to get hands on and start to write some computer vision

code with tensor flow.  bu konuyu açıklar mısj
# pytour
A python package for creating animated projections of high dimensional data.

One way we can look at the problem of high dimensional visualization is to consider the analogy of looking at a statue in a museum. A traditional approach in high dimensional
visualization would be to ask "which perspective is the best for understanding what the statue looks like?" The inuitive response is that we shouldn't look at the statue from
just one angle, or even from just a discrete collection of different angles. Instead, we should look at the statue from a variety of different angles, moving from one perspective
to another in a continuous way.

Suppose we have data `X` that lives in `R^{n x p}`. If our target visualization dimension is `d`, then an orthogonal matrix `F` in `R^{p x d}` such that `XF` is a projection of
interest is called a "frame". If `F(t)` is a continuous path of frames, then we call the continuous set of projections `XF(t)` a "tour" of the data. This python module is
constructed to take in data `X` and construct the tours `XF(t)`. Options for tours include:
- Grand Tour: We generate random frames to travel to.
- Preset Tour: We move from frame to frame specified by a user-provided list of frames. 
- Checkpoint Tour: Given a specified list of vectors, we move between frames that embed some subset of the vectors with one-off changes.
- Custom Tour: We move from frame to frame specified by a generator that specifies tuples of the next frame and the number of steps to take.


# Math Intro

### Sigmoid

$$
\sigma(x) = \frac{1}{1 + e^{-x}}
$$

### Derivative

By chainrule:

$$
\frac{\partial\sigma}{\partial x} = 
\frac{\partial\frac{1}{1 + e^{-x}}}{\partial 1 + e^{-x}} \cdot 
\frac{\partial 1 + e^{-x}}{\partial e^{-x}} \cdot
\frac{\partial e^{-x}}{\partial -x} \cdot
\frac{\partial -x}{\partial x} 
$$

Indivudual derivatives:

$$
\frac{\partial\frac{1}{1 + e^{-x}}}{\partial 1 + e^{-x}} = 
\frac{-1}{(1 + e^{-x})\cdot (1 + e^{-x})}
$$

$$
\frac{\partial 1 + e^{-x}}{\partial e^{-x}} = 1
$$

$$
\frac{\partial e^{-x}}{\partial -x} = e^{-x}
$$

$$
\frac{\partial -x}{\partial x} = - 1
$$

Combining derivatives:

$$
\frac{\partial\sigma}{\partial x} = 
\frac{-1}{(1 + e^{-x})\cdot (1 + e^{-x})} \cdot 1 \cdot e^{-x} \cdot (-1)
$$

Simplifing:

$$
\frac{\partial\sigma}{\partial x} = 
\frac{e^{-x}}{(1 + e^{-x})\cdot (1 + e^{-x})}
$$

$$
\frac{\partial\sigma}{\partial x} = 
\frac{1}{1 + e^{-x}} \cdot \frac{e^{-x}}{1 + e^{-x}}
$$

Inspecting single term:

$$
\frac{e^{-x}}{1 + e^{-x}} = \frac{1}{e^x + 1} = \sigma(-x)
$$

$$
\frac{e^{-x}}{1 + e^{-x}} = \frac{1 +e^{-x} - 1}{1 + e^{-x}} =  
\frac{1 + e^{-x}}{1 + e^{-x}} - \frac{1}{1 + e^{-x}} = 
1 - \sigma(x)
$$

Substituting for $\frac{e^{-x}}{1 + e^{-x}}$:

$$
\frac{\partial\sigma}{\partial x} = 
\frac{1}{1 + e^{-x}} \cdot \frac{e^{-x}}{1 + e^{-x}} =
\sigma(x) \cdot \sigma(-x) = \sigma(x)(1 - \sigma(x))
$$

### Task

$$
f (x, z, a, b) := y = (4ax^2 + a) + 3 + σ(z) + (σ(b))^2
$$

$$
\frac{\partial y}{\partial x} = 8ax
$$

$$
\frac{\partial y}{\partial z} = \sigma'(z)
$$

$$
\frac{\partial y}{\partial a} = 4x^2 + 1
$$

$$
\frac{\partial y}{\partial b} = 2\sigma(b)\sigma'(b)
$$

$$
\nabla y = \left[\begin{matrix}
8ax\\
\sigma(z)\\
4x^2+1\\
2\sigma(b)\sigma'(b)
\end{matrix}\right]
$$



# Missing-Kit
 The missing tool kit for MVS researchers

## MVS Main Pipeline
 - Image pre-process
   - Mask background
 - Generate SfM
   - Pick selected views
      - Feature extraction
      - Feature matching
      - Sparse reconstruction
      - Poisson generation
   - Fit rotation axis
   - Generate full SfM (optional)
      - Mask generation (from previously generated poisson mesh) 
      - Feature extraction
      - Feature matching
      - Mock initial pose
 - Triangulate
 - Bundle adjustment
 - Feature transform (optional)
 - Dense reconstruction
 - Evaluate

## Core ideas
 - **Replacement of Code Snippets**: common operations with easy interfaces
 - **Unified Numeric Interface**: all data interfaces are `np.ndarray`

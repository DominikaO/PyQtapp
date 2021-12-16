import arrayfire as af


def adaptive_threshold(img, thresh_type, window_size, constnt):
    wr = window_size
    ret_val = af.image.color_space(img, af.CSPACE.GRAY, af.CSPACE.RGB)
    if thresh_type == 0:
        wind = af.constant(1, wr, wr) / (wr * wr)
        mean = af.convolve(ret_val, wind)
        diff = mean - ret_val
        ret_val = (diff < constnt) * 0.0 + 255.0 * (diff > constnt)
    elif thresh_type == 1:
        medf = af.medfilt(ret_val, wr, wr)
        diff = medf - ret_val
        ret_val = (diff < constnt) * 0.0 + 255.0 * (diff > constnt)
    elif thresh_type == 2:
        minf = af.minfilt(ret_val, wr, wr)
        maxf = af.maxfilt(ret_val, wr, wr)
        mean = (minf + maxf) / 2.00
        diff = mean - ret_val
        ret_val = (diff < constnt) * 0.0 + 255.0 * (diff > constnt)
    ret_val = 255.0 - ret_val
    ret_val = af.image.color_space(ret_val, af.CSPACE.RGB, af.CSPACE.GRAY)
    af.image.save_image(ret_val, "PREPROCESSED.jpg")
    return ret_val

def adaptive_canny(img, threshold):
    img = af.image.color_space(img, af.CSPACE.GRAY, af.CSPACE.RGB)
    img = af.image.canny(img, low_threshold=threshold, threshold_type=af.image.CANNY_THRESHOLD.AUTO_OTSU)
    img = af.cast(img, af.Dtype.u8)
    img = af.image.color_space(img, af.CSPACE.RGB, af.CSPACE.GRAY)
    return img
def adaptive_gaussian(img, kernel_rows, kernel_cols):
    img = af.image.color_space(img, af.CSPACE.GRAY, af.CSPACE.RGB)

    kernel = af.image.gaussian_kernel(kernel_rows, kernel_cols)
    img = af.signal.convolve2(img, kernel)

    img = af.image.color_space(img, af.CSPACE.RGB, af.CSPACE.GRAY)
    return img
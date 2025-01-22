import java.awt.image.BufferedImage
import java.awt.Graphics
import javax.swing.JFrame
import javax.swing.JPanel
import java.io.File
import javax.imageio.ImageIO
import kotlin.math.*
import kotlin.math.exp

fun loadImg(filePath: String): BufferedImage {
    return ImageIO.read(File(filePath))
}

fun imgArray(image: BufferedImage): Array<Array<Triple<Int, Int, Int>>> {
    val width = image.width
    val height = image.height
    val pixels = Array(height) { Array(width) { Triple(0, 0, 0) } }
    for (y in 0 until height) {
        for (x in 0 until width) {
            val pixel = image.getRGB(x, y)
            val r = (pixel shr 16) and 0xFF
            val g = (pixel shr 8) and 0xFF
            val b = pixel and 0xFF
            pixels[y][x] = Triple(r, g, b)
        }
    }
    return pixels
}

fun toGrayscale(image: Array<Array<Triple<Int, Int, Int>>>): Array<Array<Int>> {
    val grayscale = Array(image.size) { Array(image[0].size) { 0 } }
    for (i in image.indices) {
        for (j in image[i].indices) {
            val (r, g, b) = image[i][j]
            val gray = (0.299 * r + 0.587 * g + 0.114 * b).toInt()
            grayscale[i][j] = gray
        }
    }
    return grayscale
}

fun matGauss(size: Int, sigma: Double): Array<Array<Double>> {
    val center = size / 2
    val gauss = Array(size) { Array(size) { 0.0 } }
    for (x in 0 until size) {
        for (y in 0 until size) {
            gauss[x][y] = (1 / (2 * Math.PI * sigma * sigma)) *
                    exp(-((x - center) * (x - center) + (y - center) * (y - center)) / (2 * sigma * sigma))
        }
    }
    val sum = gauss.flatten().sum()
    return gauss.map { row -> row.map { it / sum }.toTypedArray() }.toTypedArray()
}

fun filter(image: Array<Array<Int>>, kernel: Array<Array<Double>>): Array<Array<Double>> {
    val size = kernel.size
    val center = size / 2
    val blur = Array(image.size) { Array(image[0].size) { 0.0 } }
    for (i in center until image.size - center) {
        for (j in center until image[i].size - center) {
            var value = 0.0
            for (k in 0 until size) {
                for (l in 0 until size) {
                    value += image[i - center + k][j - center + l] * kernel[k][l]
                }
            }
            blur[i][j] = value
        }
    }
    return blur
}

fun sobel(image: Array<Array<Int>>): Pair<Array<Array<Double>>, Array<Array<Double>>> {
    val gx = arrayOf(
        intArrayOf(-1, 0, 1),
        intArrayOf(-2, 0, 2),
        intArrayOf(-1, 0, 1)
    )

    val gy = arrayOf(
        intArrayOf(1, 2, 1),
        intArrayOf(0, 0, 0),
        intArrayOf(-1, -2, -1)
    )

    val gradientX = Array(image.size) { Array(image[0].size) { 0.0 } }
    val gradientY = Array(image.size) { Array(image[0].size) { 0.0 } }

    for (i in 1 until image.size - 1) {
        for (j in 1 until image[i].size - 1) {
            var gxValue = 0.0
            var gyValue = 0.0

            for (k in -1..1) {
                for (l in -1..1) {
                    gxValue += (image[i + k][j + l] * gx[k + 1][l + 1])
                    gyValue += (image[i + k][j + l] * gy[k + 1][l + 1])
                }
            }
            gradientX[i][j] = gxValue
            gradientY[i][j] = gyValue
        }
    }
    return Pair(gradientX, gradientY)
}

fun calculateMagnitudeAndDirection(gradientX: Array<Array<Double>>, gradientY: Array<Array<Double>>): Pair<Array<Array<Double>>, Array<Array<Double>>> {
    val magnitude = Array(gradientX.size) { Array(gradientX[0].size) { 0.0 } }
    val direction = Array(gradientX.size) { Array(gradientX[0].size) { 0.0 } }

    for (i in gradientX.indices) {
        for (j in gradientX[i].indices) {
            magnitude[i][j] = sqrt(gradientX[i][j] * gradientX[i][j] + gradientY[i][j] * gradientY[i][j])
            direction[i][j] = Math.toDegrees(atan2(gradientY[i][j], gradientX[i][j]))
        }
    }
    return Pair(magnitude, direction)
}

fun calculateNonMaxSuppression(magnitude: Array<Array<Double>>, gradientX: Array<Array<Double>>, gradientY: Array<Array<Double>>): Array<Array<Double>> {
    val rows = magnitude.size
    val cols = magnitude[0].size
    val sub = Array(rows) { Array(cols) { 0.0 } }
    val nonMax = Array(rows) { Array(cols) { 0.0 } }
    val tgFee = Array(rows) { Array(cols) { 0.0 } }

    for (r in 0 until rows) {
        for (c in 0 until cols) {
            tgFee[r][c] = if (gradientX[r][c] != 0.0) {
                gradientY[r][c] / gradientX[r][c]
            } else {
                Double.MAX_VALUE
            }
        }
    }

    for (r in 1 until rows - 1) {
        for (c in 1 until cols - 1) {
            val angle = Math.toDegrees(atan2(gradientY[r][c], gradientX[r][c])).toInt() % 180
            when {
                (gradientX[r][c] > 0 && gradientY[r][c] > 0 && tgFee[r][c] < 2.414) -> sub[r][c] = magnitude[r][c]
                (gradientX[r][c] > 0 && gradientY[r][c] < 0 && tgFee[r][c] > -2.414) || (gradientX[r][c] < 0 && gradientY[r][c] < 0 && tgFee[r][c] < -2.414) -> {
                    sub[r][c] = magnitude[r][c]
                }
                (gradientX[r][c] > 0 && gradientY[r][c] < 0 && tgFee[r][c] < -0.414) -> sub[r][c] = magnitude[r][c]
                (gradientX[r][c] > 0 && gradientY[r][c] > 0 && tgFee[r][c] < 0.414) -> sub[r][c] = magnitude[r][c]
                (gradientX[r][c] < 0 && gradientY[r][c] > 0 && tgFee[r][c] < -0.414) -> sub[r][c] = magnitude[r][c]
                (gradientX[r][c] < 0 && gradientY[r][c] < 0 && tgFee[r][c] < 0.414) -> sub[r][c] = magnitude[r][c]
                (gradientX[r][c] < 0 && gradientY[r][c] > 0 && tgFee[r][c] > -0.414) -> sub[r][c] = magnitude[r][c]
                (gradientX[r][c] < 0 && gradientY[r][c] < 0 && tgFee[r][c] < 2.414) -> sub[r][c] = magnitude[r][c]
                else -> sub[r][c] = 0.0
            }
            val maxim = maxOf(sub[r - 1][c - 1], sub[r - 1][c], sub[r - 1][c + 1],
                sub[r][c - 1], sub[r][c], sub[r][c + 1],
                sub[r + 1][c - 1], sub[r + 1][c], sub[r + 1][c + 1])
            if (magnitude[r][c] >= maxim) {
                nonMax[r][c] = magnitude[r][c]
            }
        }
    }
    return nonMax
}

fun doubleThresholding(suppressed: Array<Array<Double>>, lowThreshold: Double, highThreshold: Double): Array<Array<Int>> {
    val thresholded = Array(suppressed.size) { Array(suppressed[0].size) { 0 } }

    for (i in suppressed.indices) {
        for (j in suppressed[i].indices) {
            when {
                suppressed[i][j] >= highThreshold -> thresholded[i][j] = 255 // Strong edge
                suppressed[i][j] >= lowThreshold -> thresholded[i][j] = 75 // Weak edge
            }
        }
    }
    return thresholded
}

fun hysteresis(thresholded: Array<Array<Int>>): Array<Array<Int>> {
    val result = Array(thresholded.size) { Array(thresholded[0].size) { 0 } }
    for (i in 1 until thresholded.size - 1) {
        for (j in 1 until thresholded[i].size - 1) {
            if (thresholded[i][j] == 255) {
                result[i][j] = 255
            } else if (thresholded[i][j] == 75) {
                for (x in -1..1) {
                    for (y in -1..1) {
                        if (thresholded[i + x][j + y] == 255) {
                            result[i][j] = 255
                        }
                    }
                }
            }
        }
    }
    return result
}

fun saveImg(grayscale: Array<Array<Int>>, filePath: String) {
    val width = grayscale[0].size
    val height = grayscale.size
    val image = BufferedImage(width, height, BufferedImage.TYPE_INT_RGB)
    for (y in 0 until height) {
        for (x in 0 until width) {
            val gray = grayscale[y][x]
            val rgb = (gray shl 16) or (gray shl 8) or gray
            image.setRGB(x, y, rgb)
        }
    }
    ImageIO.write(image, "jpg", File(filePath))
}

fun toWindow(image: BufferedImage, title: String) {
    val frame = JFrame(title)
    frame.defaultCloseOperation = JFrame.EXIT_ON_CLOSE
    frame.contentPane.add(object : JPanel() {
        override fun paintComponent(g: Graphics) {
            super.paintComponent(g)
            g.drawImage(image, 0, 0, null)
        }
        override fun getPreferredSize() = java.awt.Dimension(image.width, image.height)
    })
    frame.pack()
    frame.isVisible = true
}

fun main() {
    val imgPath = "C:/Users/Goe/PycharmProjects/cherry.jpg"
    var img = loadImg(imgPath)
    toWindow(img, "Initial Image")

    val gray = toGrayscale(imgArray(img))
    val grayPath = "C:/Users/Goe/PycharmProjects/gray.jpg"
    saveImg(gray, grayPath)
    img = loadImg(grayPath)
    toWindow(img, "Gray Image")

    val blurred = filter(gray, matGauss(5, 1.0))
    val blurPath = "C:/Users/Goe/PycharmProjects/blurred.jpg"
    saveImg(blurred.map { it.map { v -> v.toInt() }.toTypedArray() }.toTypedArray(), blurPath)
    img = loadImg(blurPath)
    toWindow(img, "Blurred Image")

    val (gradientX, gradientY) = sobel(blurred.map { it.map { v -> v.toInt() }.toTypedArray() }.toTypedArray())
    val (magnitude, direction) = calculateMagnitudeAndDirection(gradientX, gradientY)

    val suppressed = calculateNonMaxSuppression(magnitude, gradientX, gradientY)
    val lowThreshold = 15.0
    val highThreshold = 40.0
    val thresholded = doubleThresholding(suppressed, lowThreshold, highThreshold)
    val finalEdges = hysteresis(thresholded)

    val edgesPath = "C:/Users/Goe/PycharmProjects/canny_edges.jpg"
    saveImg(finalEdges, edgesPath)
    img = loadImg(edgesPath)
    toWindow(img, "Canny Edges")
}

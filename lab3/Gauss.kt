import java.awt.image.BufferedImage
import java.awt.Graphics
import javax.swing.JFrame
import javax.swing.JPanel
import java.io.File
import javax.imageio.ImageIO
import kotlin.math.exp

fun loadImg(filePath: String): BufferedImage {
    return ImageIO.read(File(filePath))
}

fun imgArray(image: BufferedImage): Array<Array<Triple<Int, Int, Int>>> {
    val width = image.width
    val height = image.height
    val pixels = Array(height) { Array(width) { Triple(0, 0, 0) } }
    for (y in 0..< height) {
        for (x in 0..< width) {
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
    for (x in 0..< size) {
        for (y in 0..< size) {
            gauss[x][y] = (1 / (2 * Math.PI * sigma * sigma)) *
                    exp(-((x - center) * (x - center) + (y - center) * (y - center)) / (2 * sigma * sigma))
        }
    }
    val sum = gauss.flatten().sum()
    return gauss.map { row -> row.map { it / sum }.toTypedArray() }.toTypedArray()
}

fun filter(image: Array<Array<Int>>, kernel: Array<Array<Double>>): Array<Array<Int>> {
    val size = kernel.size
    val center = size / 2
    val blur = Array(image.size) { Array(image[0].size) { 0 } }
    for (i in center..< image.size - center) {
        for (j in center..< image[i].size - center) {
            var value = 0.0
            for (k in 0..< size) {
                for (l in 0..< size) {
                    value += image[i - center + k][j - center + l] * kernel[k][l]
                }
            }
            blur[i][j] = value.toInt()
        }
    }
    return blur
}

fun saveImg(grayscale: Array<Array<Int>>, filePath: String) {
    val width = grayscale[0].size
    val height = grayscale.size
    val image = BufferedImage(width, height, BufferedImage.TYPE_INT_RGB)
    for (y in 0..< height) {
        for (x in 0..< width) {
            val gray = grayscale[y][x]
            val rgb = gray shl 16 or (gray shl 8) or gray
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
        override fun getPreferredSize() = kotlin.run {
            java.awt.Dimension(image.width, image.height)
        }
    })
    frame.pack()
    frame.isVisible = true
}

fun main() {
    val imgPath = "C:/edu/4-1/acom/lab3/cherry.jpg"
    var img = ImageIO.read(File(imgPath))
    toWindow(img, "initial img")
    val gray = toGrayscale(imgArray(loadImg(imgPath)))
    val grayPath = "C:/edu/4-1/acom/lab3/gray.jpg"
    saveImg(gray, grayPath)
    img = ImageIO.read(File(grayPath))
    toWindow(img, "gray img")
    val blured = filter(gray, matGauss(5, 1.0))
    val blurPath = "C:/edu/4-1/acom/lab3/blured.jpg"
    saveImg(blured, blurPath)
    img = ImageIO.read(File(blurPath))
    toWindow(img, "blured img")
}

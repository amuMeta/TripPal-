import html2canvas from 'html2canvas'
import jsPDF from 'jspdf'

const hideMapTemporarily = () => {
  const mapContainer = document.getElementById('map-container')
  if (!mapContainer) {
    return () => undefined
  }

  const previousDisplay = mapContainer.style.display
  mapContainer.style.display = 'none'
  return () => {
    mapContainer.style.display = previousDisplay
  }
}

export const useExport = () => {
  const capture = async () => {
    const element = document.querySelector('.result-page') as HTMLElement | null
    if (!element) {
      throw new Error('未找到导出区域')
    }

    const restore = hideMapTemporarily()
    try {
      return await html2canvas(element, { scale: 2, useCORS: true })
    } finally {
      restore()
    }
  }

  const exportAsPNG = async (filename: string) => {
    const canvas = await capture()
    const link = document.createElement('a')
    link.href = canvas.toDataURL('image/png')
    link.download = filename
    link.click()
  }

  const exportAsPDF = async (filename: string) => {
    const canvas = await capture()
    const imgData = canvas.toDataURL('image/png')
    const pdf = new jsPDF({ orientation: 'portrait', unit: 'mm', format: 'a4' })
    const imgWidth = 210
    const imgHeight = (canvas.height * imgWidth) / canvas.width
    pdf.addImage(imgData, 'PNG', 0, 0, imgWidth, imgHeight)
    pdf.save(filename)
  }

  return {
    exportAsPNG,
    exportAsPDF,
  }
}

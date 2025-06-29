// In-memory storage for demo purposes
let resumeStorage: any = null

export async function POST(request: Request) {
  try {
    const resumeData = await request.json()

    // Store in memory
    resumeStorage = {
      ...resumeData,
      savedAt: new Date().toISOString(),
      id: Date.now().toString(),
    }

    // Optionally save to file (uncomment if you want file persistence)
    // const filePath = join(process.cwd(), 'saved-resumes', `resume-${Date.now()}.json`)
    // await writeFile(filePath, JSON.stringify(resumeStorage, null, 2))

    console.log("Resume saved:", resumeStorage.id)

    return Response.json({
      success: true,
      message: "Resume saved successfully",
      resumeId: resumeStorage.id,
    })
  } catch (error) {
    console.error("Save resume error:", error)
    return Response.json({ success: false, error: "Failed to save resume" }, { status: 500 })
  }
}

export async function GET() {
  return Response.json({
    success: true,
    resume: resumeStorage,
  })
}

const API_BASE_URL = "http://127.0.0.1:8000";

export const generateQuiz = async (contextText, topic, difficulty) => {
  try {
    const response = await fetch(`${API_BASE_URL}/api/generate-quiz`, {
      method: "POST",
      headers: {
        "Content-Type": "application/json",
      },
      body: JSON.stringify({
        context_text: contextText,
        topic: topic,
        difficulty: difficulty,
        num_questions: 5,
      }),
    });

    if (!response.ok) {
      const errorData = await response.json().catch(() => ({}));

      if (response.status === 429 || errorData.detail?.includes("429")) {
        throw new Error("SERVICE_AT_CAPACITY");
      }

      throw new Error(errorData.detail || "Failed to generate quiz");
    }

    return await response.json();
  } catch (error) {
    throw error;
  }
};

export const generateSummary = async (contextText, topic) => {
  try {
    const response = await fetch(`${API_BASE_URL}/api/generate-summary`, {
      method: "POST",
      headers: {
        "Content-Type": "application/json",
      },
      body: JSON.stringify({
        context_text: contextText,
        topic: topic,
      }),
    });

    if (!response.ok) {
      const errorData = await response.json().catch(() => ({}));

      if (response.status === 429 || errorData.detail?.includes("429")) {
        throw new Error("SERVICE_AT_CAPACITY");
      }

      throw new Error(errorData.detail || "Failed to generate summary");
    }

    return await response.json();
  } catch (error) {
    throw error;
  }
};

export const generateGlossary = async (contextText, topic) => {
  try {
    const response = await fetch(`${API_BASE_URL}/api/generate-glossary`, {
      method: "POST",
      headers: {
        "Content-Type": "application/json",
      },
      body: JSON.stringify({
        context_text: contextText,
        topic: topic,
      }),
    });

    if (!response.ok) {
      const errorData = await response.json().catch(() => ({}));

      if (response.status === 429 || errorData.detail?.includes("429")) {
        throw new Error("SERVICE_AT_CAPACITY");
      }

      throw new Error(errorData.detail || "Failed to generate glossary");
    }

    return await response.json();
  } catch (error) {
    throw error;
  }
};

export const uploadPDF = async (file) => {
  try {
    const formData = new FormData();
    formData.append('file', file);

    const response = await fetch(`${API_BASE_URL}/api/upload-pdf`, {
      method: "POST",
      body: formData,
    });

    if (!response.ok) {
      const errorData = await response.json().catch(() => ({}));
      throw new Error(errorData.detail || "Failed to upload PDF");
    }

    return await response.json();
  } catch (error) {
    throw error;
  }
};
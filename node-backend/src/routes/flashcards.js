const express = require("express");
const router = express.Router();
const { PrismaClient } = require("@prisma/client");
const axios = require("axios");

const prisma = new PrismaClient();

// 1. Create content (a topic)
router.post("/content", async (req, res) => {
  const { title, subject, content } = req.body;

  try {
    const newTopic = await prisma.topic.create({
      data: {
        title,
        subject,
        content,
      },
    });
    res.json({ topic: newTopic });
  } catch (error) {
    console.error("Error creating topic:", error);
    res.status(500).json({
      error: "Failed to create topic",
      details: error.message,
    });
  }
});

// 2. Generate flashcards (calls Python microservice)
router.post("/content/:id/generate", async (req, res) => {
  const { id } = req.params;

  try {
    const topic = await prisma.topic.findUnique({
      where: { id },
    });

    if (!topic) {
      return res.status(404).json({ error: "Topic not found" });
    }

    const response = await axios.post(
      process.env.PYTHON_MICROSERVICE_URL + "/create_card",
      {
        id: topic.id,
        subject: topic.subject || "General",
        title: topic.title,
        content: topic.content,
      },
      {
        timeout: 10000, // 10 second timeout
        headers: {
          "Content-Type": "application/json",
        },
      }
    );

    // Add download link to response
    const result = {
      ...response.data,
      download_link: `${process.env.PYTHON_MICROSERVICE_URL}/download/${response.data.deck_id}`,
    };

    res.json(result);
  } catch (error) {
    console.error("Error generating flashcard:", error);

    let errorMessage = "Failed to generate flashcard";
    let errorDetails = {};

    if (error.response) {
      // The request was made and the server responded with a status code
      errorMessage = error.response.data.error?.message || errorMessage;
      errorDetails = error.response.data.error || {};
    } else if (error.request) {
      // The request was made but no response was received
      errorMessage = "No response from flashcard service";
    }

    res.status(500).json({
      error: errorMessage,
      details: errorDetails,
      stack: process.env.NODE_ENV === "development" ? error.stack : undefined,
    });
  }
});

module.exports = router;

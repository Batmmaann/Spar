"use client"

import React, { useState } from "react"
import { motion } from "framer-motion"

export default function Home() {
  const [uploading, setUploading] = useState(false)
  const [message, setMessage] = useState("")

  const handleUpload = async (e: React.FormEvent<HTMLFormElement>) => {
    e.preventDefault()
    setUploading(true)
    setMessage("")

    const file = (new FormData(e.currentTarget)).get("file") as File
    if (!file) {
      setMessage("⚠️ Please select a video to upload")
      setUploading(false)
      return
    }

    try {
      const res = await fetch("http://localhost:8000/upload", {
        method: "POST",
        body: new FormData(e.currentTarget),
      })
      if (!res.ok) throw new Error()
      const { message: success } = await res.json()
      setMessage(`✅ ${success}`)
    } catch {
      setMessage("❌ Failed to upload — try again")
    } finally {
      setUploading(false)
    }
  }

  return (
    <motion.main
      initial={{ opacity: 0 }}
      animate={{ opacity: 1 }}
      transition={{ duration: 0.5 }}
      className="min-h-screen bg-gradient-to-br from-gray-900 to-black text-white flex flex-col items-center justify-center px-6 py-12 space-y-12"
    >
      <motion.section
        initial={{ y: -30 }}
        animate={{ y: 0 }}
        transition={{ delay: 0.2 }}
        className="max-w-3xl text-center space-y-6"
      >
        <h1 className="text-5xl font-extrabold drop-shadow-lg">
          SPAR  
        </h1>
        <p className="text-xl text-gray-300">
          Transform raw match footage into actionable insights. Upload a game video to automatically track player movement, calculate FIFA‑style ratings, and discover rising stars.
        </p>
        <ul className="grid grid-cols-1 md:grid-cols-3 gap-6 text-left mt-8">
          {[
            "🚀 Instant Player Ratings",
            "📊 Interactive Stats & Charts",
            "💰 Estimated Market Value"
          ].map((feature) => (
            <li key={feature} className="bg-gray-800 rounded-lg p-4 shadow-md hover:bg-gray-700 transition">
              {feature}
            </li>
          ))}
        </ul>
      </motion.section>

      <motion.form
        onSubmit={handleUpload}
        initial={{ scale: 0.8 }}
        animate={{ scale: 1 }}
        transition={{ delay: 0.4 }}
        className="relative bg-gradient-to-r from-indigo-600 via-purple-600 to-pink-600 p-1 rounded-3xl shadow-2xl w-full max-w-md"
      >
        <div className="bg-gray-900 rounded-2xl p-8 space-y-6">
          <label className="block text-lg font-semibold">Upload Your Match Video</label>
          <input
            type="file"
            name="file"
            accept="video/*"
            className="block w-full file:rounded-full file:px-6 file:py-3 file:bg-green-500 file:text-white hover:file:bg-green-600"
          />

          <motion.button
            type="submit"
            disabled={uploading}
            whileHover={{ scale: uploading ? 1 : 1.05 }}
            whileTap={{ scale: 0.95 }}
            className={`w-full py-3 rounded-full text-xl font-semibold text-white shadow-lg transition ${
              uploading
                ? "bg-green-700 opacity-50 cursor-not-allowed"
                : "bg-gradient-to-r from-green-400 to-teal-500 hover:from-green-500 hover:to-teal-600 animate-pulse"
            }`}
          >
            {uploading ? "Analyzing..." : "Analyze"}
          </motion.button>

          {message && (
            <motion.div
              initial={{ opacity: 0 }}
              animate={{ opacity: 1 }}
              className="text-center text-sm text-gray-300 mt-2"
            >
              {message}
            </motion.div>
          )}
        </div>
      </motion.form>
    </motion.main>
  )
}

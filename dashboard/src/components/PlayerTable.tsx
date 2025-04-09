"use client"

import React from "react"
import Link from "next/link"
import { motion } from "framer-motion"

type Player = {
  id: number
  track_id: number
  pace: number
  shooting: number
  passing: number
  dribbling: number
  defending: number
  physical: number
  overall: number
  value: number
}

interface PlayerTableProps {
  players: Player[]
}

export default function PlayerTable({ players }: PlayerTableProps) {
  return (
    <div className="overflow-x-auto">
      <motion.table
        initial={{ opacity: 0 }}
        animate={{ opacity: 1 }}
        transition={{ delay: 0.3, duration: 0.8 }}
        className="w-full table-auto bg-gray-800 rounded-lg"
      >
        <thead className="bg-gray-700">
          <tr>
            {["ID","Overall","Value (SAR)","Pace","Shooting","Passing","Dribbling","Defending","Physical"].map(col => (
              <th key={col} className="px-4 py-3 text-left">
                {col}
              </th>
            ))}
          </tr>
        </thead>
        <tbody>
          {players.map(p => (
            <motion.tr
              key={p.id}
              whileHover={{ scale: 1.02 }}
              transition={{ type: "spring", stiffness: 300 }}
              className="border-b border-gray-700 hover:bg-gray-700"
            >
              <td className="px-4 py-2">
                <Link href={`/players/${p.id}`} className="hover:underline text-green-300">
                  Player {p.id}
                </Link>
              </td>
              <td className="px-4 py-2">{p.overall}</td>
              <td className="px-4 py-2">${p.value.toLocaleString()}</td>
              <td className="px-4 py-2">{p.pace}</td>
              <td className="px-4 py-2">{p.shooting}</td>
              <td className="px-4 py-2">{p.passing}</td>
              <td className="px-4 py-2">{p.dribbling}</td>
              <td className="px-4 py-2">{p.defending}</td>
              <td className="px-4 py-2">{p.physical}</td>
            </motion.tr>
          ))}
        </tbody>
      </motion.table>
    </div>
  )
}

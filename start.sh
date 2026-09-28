#!/bin/bash
echo "🚀 Starting CineScraper Unified Worker..."

while true; do
  echo "🎬 Starting CineScraper..."
  python cinescraper.py
  echo "⚠️ Process exited. Restarting in 5 seconds..."
  sleep 5
done

// src/data/hipparcos.ts
export type HipparcosEntry = {
  id: number;
  ra: number;  // Right Ascension in degrees
  dec: number; // Declination in degrees
};

const hipparcosCache = new Map<number, HipparcosEntry>();

export async function loadHipparcosData(): Promise<void> {
  try {
    console.log('Loading hip_main.dat...');
    const response = await fetch('/hip_main.dat');
    if (!response.ok) {
      throw new Error(`Failed to fetch hip_main.dat: ${response.status} ${response.statusText}`);
    }
    const text = await response.text();
    const lines = text.split('\n');
    console.log(`Loaded ${lines.length} lines from hip_main.dat`);
    
    let parsed = 0;
    for (const line of lines) {
      if (line.startsWith('H|')) {
        const id = parseInt(line.substring(2, 14).trim());
        if (isNaN(id)) continue;
        
        // Parse RA: columns 15-28 (HH MM SS.SS format)
        const raStr = line.substring(15, 28).trim();
        const raMatch = raStr.match(/(\d+)\s+(\d+)\s+([\d.]+)/);
        
        // Parse Dec: columns 29-42 (±DD MM SS.S format)
        const decStr = line.substring(29, 42).trim();
        const decMatch = decStr.match(/([+-]?)(\d+)\s+(\d+)\s+([\d.]+)/);
        
        if (raMatch && decMatch) {
          const raHours = parseFloat(raMatch[1]);
          const raMinutes = parseFloat(raMatch[2]);
          const raSeconds = parseFloat(raMatch[3]);
          const ra = (raHours + raMinutes / 60 + raSeconds / 3600) * 15; // Convert to degrees
          
          const decSign = decMatch[1] === '-' ? -1 : 1;
          const decDegrees = parseFloat(decMatch[2]);
          const decMinutes = parseFloat(decMatch[3]);
          const decSeconds = parseFloat(decMatch[4]);
          const dec = decSign * (decDegrees + decMinutes / 60 + decSeconds / 3600);
          
          hipparcosCache.set(id, { id, ra, dec });
          parsed++;
        }
      }
    }
    console.log(`Successfully parsed ${parsed} Hipparcos entries`);
  } catch (error) {
    console.error('Failed to load Hipparcos data:', error);
    throw error;
  }
}

export function getHipparcosEntry(catalogId: number): HipparcosEntry | null {
  return hipparcosCache.get(catalogId) || null;
}

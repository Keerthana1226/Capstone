const path = require('path');
const { spawn } = require('child_process');

// POST /api/rotation-plan/run-recommendation
exports.runCropRecommendation = (req, res) => {
  const { last_crop, month, season } = req.body;

  if (!last_crop) {
    return res.status(400).json({ error: 'Missing last_crop in request body' });
  }

  const scriptPath = path.join(__dirname, 'rl', 'recommend_crop.py');
  const pyProcess = spawn('python', [scriptPath, '--json']); // ✅ ensure JSON output

  let output = '';
  let errorOutput = '';

  pyProcess.stdout.on('data', (data) => {
    output += data.toString();
  });

  pyProcess.stderr.on('data', (data) => {
    errorOutput += data.toString();
  });

  // ✅ Properly formatted input to Python script
  pyProcess.stdin.write(`${last_crop}\n`);
  if (month) {
    pyProcess.stdin.write(`${month}\n`);
  } else if (season) {
    pyProcess.stdin.write(`${season}\n`);
  } else {
    pyProcess.stdin.write(`\n`);
  }
  pyProcess.stdin.end();

  pyProcess.on('close', (code) => {
    if (errorOutput) {
      console.error('❌ Python error:', errorOutput);
    }

    try {
      const parsed = JSON.parse(output);
      if (parsed.error) {
        return res.status(400).json({ error: parsed.error });
      }
      return res.status(200).json(parsed); // { recommendations: [...] }
    } catch (err) {
      console.error('❌ Failed to parse Python output:', err.message);
      console.error('Raw output was:', output);
      return res.status(500).json({
        error: 'Failed to parse output from Python script.',
        raw: output
      });
    }
  });
};

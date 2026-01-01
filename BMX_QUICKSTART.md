# 🚴 BMX Terminal Quick Start Guide

Get started with Freestyle BMX Terminal Scripting in 5 minutes!

## 🎯 What is BMX Terminal?

BMX Terminal transforms boring command execution into an exciting freestyle BMX experience. Perform tricks to run commands, chain combos for bonuses, and compete with Mario characters!

## 🚀 Quick Start (3 Steps)

### Step 1: Open the Interface

Open `terminals/bmx-terminal.html` in your web browser:

```bash
cd mongoose.os
open terminals/bmx-terminal.html
# or
firefox terminals/bmx-terminal.html
# or just drag the file to your browser
```

### Step 2: Try Your First Trick

In the terminal input, type:
```bash
wheelie echo "Hello BMX!"
```

Press Enter or click Execute. You just performed your first BMX trick! 🎉

### Step 3: Chain a Combo

Try this combo sequence:
```bash
wheelie ls
bunnyhop cd ~
```

Watch as you get combo bonuses! 🌟

## 🎮 Basic Commands

### Execute with Tricks
```bash
# Simple commands
wheelie ls -la
bunnyhop cd projects
tailwhip cat file.txt

# Complex commands
backflip npm install
grind python train.py
```

### System Commands
```bash
bmx help              # Show help
bmx status            # Show stats
bmx theme mario       # Switch theme
bmx pedal 5           # Charge energy
```

### Quick Tricks Panel
Click any trick button in the sidebar to add it to your command!

## 🎨 Try Different Themes

Click theme buttons in the sidebar:
- 🍄 Mario - Mushroom Kingdom
- 🔌 Electronics - Circuit boards
- 🧪 Chemistry - Laboratory
- 🤖 Robotics - Robot factory
- ✨ And 7 more!

## ⚡ Energy System

1. **Watch the energy bar** - It shows your capacitor charge
2. **Click "Pedal to Charge"** - Charges your capacitor
3. **Execute tricks** - Consumes energy
4. **Energy decays** - Passive decay over time

## 🌟 Unlock Combos

Try these combos for bonus multipliers:

**Super Jump** (1.5x):
```bash
wheelie echo test
bunnyhop echo test
```

**Ultra Fast Compile** (2.0x):
```bash
tailwhip echo test
backflip echo test
```

**Quantum Optimization** (2.5x):
```bash
grind echo test
manual echo test
bunnyhop echo test
```

## 🏆 Track Your Progress

- **Score** - Points from tricks and combos
- **Tricks** - Total tricks performed
- **Combos** - Combo chains completed
- **Theme** - Current theme emoji

## 🎯 Pro Tips

1. **Keep energy high** - Charge before big tricks
2. **Plan combos** - Think ahead for multipliers
3. **Try all themes** - Each has unique bonuses
4. **Watch for achievements** - Popups show unlocks

## 📱 Advanced Features

### JavaScript API
```javascript
// In browser console
bmx.trick('wheelie', 'ls');
bmx.theme('electronics');
bmx.pedal(10);
bmx.status();
bmx.suggest();  // Get combo suggestions
```

### Character Selection
```javascript
bmx.character('mario');  // Mario on BMX (1.2x bonus)
bmx.character('luigi');  // Luigi on skateboard (1.3x bonus)
```

### Custom Integration
```javascript
// Integrate with your own code
const result = await window.bmxTerminal.executeTrick('wheelie', 'your-command');
console.log(`Score: ${result.points}, Total: ${result.totalScore}`);
```

## 🧪 Run Demo & Tests

1. Open browser console (F12)
2. Type: `const demo = new BMXTerminalDemo(); demo.runAll();`
3. Watch all features demo in console

Or click the "🧪 Run Demo & Tests" button (bottom right)

## 🎓 Learning Path

### Beginner (First 10 minutes)
1. ✅ Try basic tricks (wheelie, bunnyhop)
2. ✅ Charge capacitor
3. ✅ Switch 2-3 themes
4. ✅ Execute 10 commands

### Intermediate (Next 20 minutes)
1. ✅ Complete first combo
2. ✅ Try all 8 tricks
3. ✅ Unlock first achievement
4. ✅ Reach 1,000 points

### Advanced (Next hour)
1. ✅ Master all combos
2. ✅ Try all 11 themes
3. ✅ Unlock token formula combo
4. ✅ Reach 10,000 points
5. ✅ Use MRW characters

### Expert (Ongoing)
1. ✅ Optimize combo chains
2. ✅ Compete on leaderboard
3. ✅ Unlock all achievements
4. ✅ Create custom integrations

## 🆘 Troubleshooting

### "Not enough energy" error
- Click "Pedal to Charge" button
- Energy decays over time, keep it above 50%

### Combo not detected
- Tricks must be consecutive
- Check combo requirements in help
- Some combos need 3+ tricks

### Theme not changing
- Make sure to click theme button
- Check console for errors
- Refresh page if needed

### Terminal not responding
- Refresh browser page
- Check console for errors
- Make sure all JS files loaded

## 📚 Next Steps

1. **Read full docs**: See `BMX_TERMINAL_README.md`
2. **Check examples**: See `bmx-integration-example.js`
3. **Run tests**: See `bmx-demo.js`
4. **Explore code**: Check the `tricks/`, `themes/`, and `scoring/` folders

## 🎮 Fun Challenges

### Challenge 1: Combo Master
Complete all 10+ combos in one session

### Challenge 2: Theme Explorer
Try all 11 themes and score 100+ points in each

### Challenge 3: Energy Efficient
Execute 20 tricks while maintaining 70%+ energy

### Challenge 4: Speed Run
Get 5,000 points in under 5 minutes

### Challenge 5: Perfect Chain
Execute 10 tricks in a row without breaking combo chain

## 💡 Did You Know?

- Each theme has unique obstacles and bonuses
- Token formula combos award bonus tokens
- Character special moves have unique effects
- Physics engine calculates real trick heights
- Achievements unlock at various milestones
- Leaderboard tracks top 100 scores

## 🚴 Ready to Ride!

You're all set! Start with simple tricks, experiment with combos, and have fun making command execution exciting!

**Remember**: It's not just about running commands - it's about doing it with style! 😎

---

**Need help?** Check the full documentation in `BMX_TERMINAL_README.md`

**Happy Riding!** 🚴‍♂️💨

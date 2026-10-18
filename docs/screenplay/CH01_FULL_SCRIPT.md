# Chapter 1 — full production screenplay



Canonical dialogue lives verbatim here and in [dialogue](CH01_DIALOGUE.md). P1 is Adrian; P2 Noah. Six authored scenes include continuous playable action; no omitted off-screen conversations. Total target 2,160 seconds (36 minutes), including 360 seconds cinematics. Estimates require playtesting. Age rating target: mature thriller; no graphic torture.



## Shared presentation rules



Local split-screen remains vertical during play. Both ready prompts precede synchronized full-screen cinematics; letterbox replaces both views only after both input contexts lock. Return uses 0.4 s blend to each third-person rig; never leave one player active under a cinematic. Each subtitle shows speaker, stable line ID and exact text; optional barks queue behind plot lines. No overlapping intelligible speech. Named voices are performance specifications, not acquired recordings.





## CH01_M01_SC01 — NEW BLOOD



1. **Scene ID:** CH01_M01_SC01; principal cutscene CH01_M01_CS01.

2. **Title:** NEW BLOOD.

3. **Location:** Intake and east cell landing. See mission [M01](../missions/CH01_MISSION_01.md).

4. **Time:** 18 October 2028, 07:10. One continuous day; no unexplained time jump within scene.

5. **Duration:** 330s total; 65s cinematic allocation, 265s playable estimate.

6. **Present:** RUSK, NOAH, ADRIAN, GUARD; two silent holding-bay inmates. Recording in M05 is an unidentified cached voice, not proof of Elena's current location.

7. **Purpose:** Establish unequal experience, threatened identity and the VANTAGE connection without explaining the conspiracy.

8. **Environment:** ENV_INTAKE, ENV_CELLBLOCK. Required readable routes, accessible interaction marks and camera clearance; see environment build specifications.

9. **Starting positions:** Noah at intake origin (0,0,0), facing north; Rusk (0,0,-2). Adrian behind barred holding bay (3,0,-4), facing west. Coordinates local to intake; Godot -Z is north.

10. **Camera:** Begin with shot CH01_M01_CS01_SH01, then third-person P1/P2. See [shot list](CH01_CAMERA_SHOTS.md). Gameplay camera at 1.6m height, 2.8m trailing, collision retracts to 0.45m; interior gate framing must retain partner visibility.

11. **Lighting:** Cool overcast window key, practical ceiling strips; badge readable under desk task light.

12. **Sound:** Bus diesel fades outside; ocean through high vent; keys and distant doors. No score until badge insert.

13. **Animation:** Noah protects photo, opens hands for search, changes overshirt off camera, walks escort route. Rusk checks cuffs, tags photo, then returns approved paper photograph before escort. Adrian rises from bench without approaching bars. Contacts require authored alignment markers; no assumed animation availability.

14. **Complete dialogue:** Main sequence follows order below. Idle/retry lines only fire under named conditions; they are not spoken during canonical forward progress.



[CH01_M01_DLG001] RUSK (clipped, guarded; 3.3s; main sequence): "Hands where I can see them. Name."



[CH01_M01_DLG002] NOAH (intimate, tense; 3.3s; main sequence): "Noah Reyes. My property stays with me."



[CH01_M01_DLG003] RUSK (clipped, guarded; 4.1s; main sequence): "Your name does. The rest goes in the tray."



[CH01_M01_DLG004] NOAH (intimate, tense; 4.1s; main sequence): "That photograph is all I have of my sister."



[CH01_M01_DLG005] RUSK (clipped, guarded; 2.9s; main sequence): "Then remember what she looks like."



[CH01_M01_DLG006] ADRIAN (low, controlled; 2.1s; main sequence): "Ask for a receipt."



[CH01_M01_DLG007] NOAH (intimate, tense; 2.5s; main sequence): "You running the front desk?"



[CH01_M01_DLG008] ADRIAN (low, controlled; 2.9s; main sequence): "No. I know what disappears here."



[CH01_M01_DLG009] RUSK (clipped, guarded; 2.0s; main sequence): "Cross. Sit down."



[CH01_M01_DLG010] GUARD (clipped, guarded; 4.5s; main sequence): "Contract security signed the delivery. Same seal as last week."



[CH01_M01_DLG011] NOAH (intimate, tense; 3.3s; main sequence): "The triangle. Where did that come from?"



[CH01_M01_DLG012] RUSK (clipped, guarded; 2.0s; main sequence): "Eyes forward."



[CH01_M01_DLG013] ADRIAN (low, controlled; 2.1s; main sequence): "VANTAGE. You know them?"



[CH01_M01_DLG014] NOAH (intimate, tense; 4.1s; main sequence): "I know a crate I should never have opened."



[CH01_M01_DLG015] RUSK (clipped, guarded; 2.9s; main sequence): "Thirteen, Cross. Fourteen, Reyes. Welcome home."



[CH01_M01_DLG016] ADRIAN (low, controlled; 2.9s; main sequence): "Keep your voice below the pipes."



[CH01_M01_DLG017] NOAH (intimate, tense; 3.7s; main sequence): "You first. How do you know that name?"



[CH01_M01_DLG018] ADRIAN (low, controlled; 4.9s; main sequence): "Because somebody killed a man and left it in my file."



[CH01_M01_DLG019] NOAH (intimate, tense; 3.3s; main sequence): "A receipt. You said I needed one."



[CH01_M01_DLG020] RUSK (clipped, guarded; 6.5s; main sequence): "Property number forty-two. Keep the photograph. Lose the receipt and the rest was never here."



[CH01_M01_DLG021] GUARD (clipped, guarded; 3.3s; intake idle after 20s): "Step onto the painted mark. Both feet."



[CH01_M01_DLG022] ADRIAN (low, controlled; 3.3s; badge reminder): "The stamp, Reyes. Look at the stamp."



15. **Player actions and stage direction:** Escort Noah to search mark. P1 watches through bars and selects the stamped badge for a focus interaction while P2 submits possessions. Rusk moves Noah to east cell 14; Adrian is assigned adjacent cell 13. P1 and P2 each inspect their sink and barred door to establish controls.

16. **Cooperative mechanics:** Parallel observation: neither player can see both the property receipt and badge. Both acknowledge observations before cell assignment proceeds; no dexterity gate.

17. **Objectives and triggers:** OBJ001 submit property; OBJ002 P1 inspect badge; OBJ003 both enter assigned cell marks. Trigger CS01 on both ready, never on only P2 crossing. IDs are CH01_M01_OBJ001 onward in listed order. Checkpoint CP01_A at scene entry, CP01_B after final reversible puzzle; checkpoint restores both players, props, patrol phase and dialogue consumed flags atomically. No checkpoint inside locked cinematic.

18. **Transitions:** Main cinematic CH01_M01_CS01, divided into shots in the camera sheet. Opening shot may establish space, dialogue is spread across authored interactions as assigned below; never cram all dialogue into cinematic allocation. End fades only where camera sheet calls one. Completion grants next mission together; cancellation/reload restores pre-trigger state.

19. **Required assets:** CHAR_ADRIAN, CHAR_NOAH, CHAR_RUSK, CHAR_GUARD, CHAR_INMATE, PROP_PHOTO, PROP_VANTAGE_BADGE, AUDIO_PRISON, ANIM_HUMANOID, MAT_CONCRETE, MAT_METAL, UI_SUBTITLES. These are requirements, not a claim that files exist. Every performance needs the appropriate clip in ANIM_HUMANOID; missing clips are blockers for final production.

20. **Ending state:** Both confined on east landing. Photo tagged as approved paper effects and returned to Noah before cell assignment; other property stored in locker42. Adrian knows Noah recognized the mark; Noah knows Adrian noticed.



**Dialogue staging:** DLG001–006 at property tray;007–012 at badge/search desk;013–014 at bars after badge inspection;015 on cell assignment;016–018 in cells through pipe;019–020 receipt handoff before doors lock. This last handoff occurs before final closed-door camera hold. Optional idle/retry lines fire only under their named condition. Plot dialogue waits for hearing distance and preceding line completion.






## CH01_M02_SC01 — TROUBLE IN THE YARD



1. **Scene ID:** CH01_M02_SC01; principal cutscene CH01_M02_CS01.

2. **Title:** TROUBLE IN THE YARD.

3. **Location:** Exercise yard. See mission [M02](../missions/CH01_MISSION_02.md).

4. **Time:** 18 October 2028, 10:20. One continuous day; no unexplained time jump within scene.

5. **Duration:** 360s total; 45s cinematic allocation, 315s playable estimate.

6. **Present:** SILAS, NOAH, ADRIAN, GUARD; two silent north-fence inmates. Recording in M05 is an unidentified cached voice, not proof of Elena's current location.

7. **Purpose:** Earn cooperation through a nonlethal confrontation and establish the first shared lead.

8. **Environment:** ENV_YARD. Required readable routes, accessible interaction marks and camera clearance; see environment build specifications.

9. **Starting positions:** Noah beside south exercise bench (0,0,0). Adrian at water tap (5,0,-4). Silas at (0,0,-2); two inmates observe from north fence.

10. **Camera:** Begin with shot CH01_M02_CS01_SH01, then third-person P1/P2. See [shot list](CH01_CAMERA_SHOTS.md). Gameplay camera at 1.6m height, 2.8m trailing, collision retracts to 0.45m; interior gate framing must retain partner visibility.

11. **Lighting:** Hard morning sun softened by coastal haze; tower searchlight off.

12. **Sound:** Fence rattle, gulls, basketball impacts; impacts duck during confrontation.

13. **Animation:** Silas blocks path and shoves shoulder once. Adrian places open hand between them; Noah rolls loose basketball toward west fence. Guard turns to rattle; both retreat with hands visible. Contacts require authored alignment markers; no assumed animation availability.

14. **Complete dialogue:** Main sequence follows order below. Idle/retry lines only fire under named conditions; they are not spoken during canonical forward progress.



[CH01_M02_DLG001] SILAS (natural, understated; 2.5s; main sequence): "Fourteen. You borrowed my bench."



[CH01_M02_DLG002] NOAH (intimate, tense; 2.0s; main sequence): "It looked empty."



[CH01_M02_DLG003] SILAS (natural, understated; 2.9s; main sequence): "That was the invitation to ask."



[CH01_M02_DLG004] ADRIAN (low, controlled; 5.7s; main sequence): "He is on laundry. You break his hands, you wash your own sheets."



[CH01_M02_DLG005] SILAS (natural, understated; 2.5s; main sequence): "You vouching for him, Cross?"



[CH01_M02_DLG006] ADRIAN (low, controlled; 2.9s; main sequence): "I am saving you a chore."



[CH01_M02_DLG007] ADRIAN (low, controlled; 2.9s; main sequence): "Reyes. The ball. West fence. Easy."



[CH01_M02_DLG008] NOAH (intimate, tense; 2.5s; main sequence): "You want me to play?"



[CH01_M02_DLG009] ADRIAN (low, controlled; 2.9s; main sequence): "I want him looking somewhere else."



[CH01_M02_DLG010] GUARD (clipped, guarded; 3.3s; main sequence): "Away from the fence! All of you!"



[CH01_M02_DLG011] SILAS (natural, understated; 3.3s; main sequence): "This buys you a morning. Nothing else."



[CH01_M02_DLG012] NOAH (intimate, tense; 2.9s; main sequence): "You always make friends this quickly?"



[CH01_M02_DLG013] ADRIAN (low, controlled; 2.9s; main sequence): "Only when I need somebody alive."



[CH01_M02_DLG014] NOAH (intimate, tense; 5.7s; main sequence): "My sister Elena was on that run. They told me the boat burned."



[CH01_M02_DLG015] ADRIAN (low, controlled; 2.5s; main sequence): "Did you see her body?"



[CH01_M02_DLG016] NOAH (intimate, tense; 4.9s; main sequence): "I saw a bag. They would not let me open it."



[CH01_M02_DLG017] ADRIAN (low, controlled; 4.9s; main sequence): "The man I was accused of killing was investigating VANTAGE transfers."



[CH01_M02_DLG018] NOAH (intimate, tense; 4.1s; main sequence): "So we have a logo and two dead people."



[CH01_M02_DLG019] ADRIAN (low, controlled; 4.1s; main sequence): "We have people who want us to stop asking."



[CH01_M02_DLG020] NOAH (intimate, tense; 2.5s; main sequence): "Laundry. We keep asking there."



[CH01_M02_DLG021] SILAS (natural, understated; 2.0s; distraction idle after 20s): "Finished thinking?"



[CH01_M02_DLG022] ADRIAN (low, controlled; 3.3s; missed distraction reset): "Easy. We try when he turns again."



[CH01_M02_DLG023] NOAH (intimate, tense; 2.9s; optional skeptical stance; reconverges before next objective): "I do not trust you yet."



[CH01_M02_DLG024] ADRIAN (low, controlled; 3.3s; optional skeptical stance; reconverges before next objective): "Then trust what we can both see."



15. **Player actions and stage direction:** P2 approaches exercise bench; Silas blocks exit. P1 walks to marked mediation space. P1 holds Silas attention in conversation while P2 rolls loose ball into empty fence section; guard looks west. Players withdraw together to tap alcove before whistle.

16. **Cooperative mechanics:** Conversation window waits for P2 ready. Distraction never injures an NPC. Missing timing resets standoff rather than forcing combat.

17. **Objectives and triggers:** OBJ001 both enter yard; OBJ002 P1 begin mediation and P2 roll ball; OBJ003 both reach tap alcove. Trigger CS01 once in alcove. IDs are CH01_M02_OBJ001 onward in listed order. Checkpoint CP02_A at scene entry, CP02_B after final reversible puzzle; checkpoint restores both players, props, patrol phase and dialogue consumed flags atomically. No checkpoint inside locked cinematic.

18. **Transitions:** Main cinematic CH01_M02_CS01, divided into shots in the camera sheet. Opening shot may establish space, dialogue is spread across authored interactions as assigned below; never cram all dialogue into cinematic allocation. End fades only where camera sheet calls one. Completion grants next mission together; cancellation/reload restores pre-trigger state.

19. **Required assets:** CHAR_ADRIAN, CHAR_NOAH, CHAR_RUSK, CHAR_SILAS, CHAR_GUARD, CHAR_INMATE, AUDIO_PRISON, ANIM_HUMANOID, MAT_CONCRETE, MAT_METAL, UI_SUBTITLES. These are requirements, not a claim that files exist. Every performance needs the appropriate clip in ANIM_HUMANOID; missing clips are blockers for final production.

20. **Ending state:** Adrian and Noah agree to exchange information in laundry inspection detail. Silas remains hostile, neither protagonist becomes a murderer.



**Dialogue staging:** DLG001–006 confrontation opening;007–009 while P1 mediates and P2 prepares ball;010guardreaction after ball;011Silasretreat;012–020 tap alcove conversation. Optional skeptical stance after020, then next mission. Optional idle/retry lines fire only under their named condition. Plot dialogue waits for hearing distance and preceding line completion.






## CH01_M03_SC01 — THE WORKSHOP



1. **Scene ID:** CH01_M03_SC01; principal cutscene CH01_M03_CS01.

2. **Title:** THE WORKSHOP.

3. **Location:** Laundry workshop and service office. See mission [M03](../missions/CH01_MISSION_03.md).

4. **Time:** 18 October 2028, 14:05. One continuous day; no unexplained time jump within scene.

5. **Duration:** 420s total; 50s cinematic allocation, 370s playable estimate.

6. **Present:** MARA, NOAH, RUSK, ADRIAN. Recording in M05 is an unidentified cached voice, not proof of Elena's current location.

7. **Purpose:** Create a credible route and first deliberate pact; seed Rusk coercion through a clinic envelope.

8. **Environment:** ENV_WORKSHOP. Required readable routes, accessible interaction marks and camera clearance; see environment build specifications.

9. **Starting positions:** Adrian at press operator mark (0,0,0); Noah at lint inspection hatch (2,0,0). Dr Mara Sen at medical textile table (4,0,-2); Rusk at office door (0,0,-6).

10. **Camera:** Begin with shot CH01_M03_CS01_SH01, then third-person P1/P2. See [shot list](CH01_CAMERA_SHOTS.md). Gameplay camera at 1.6m height, 2.8m trailing, collision retracts to 0.45m; interior gate framing must retain partner visibility.

11. **Lighting:** Warm press task lights against cold strip ceiling; backlit steam never obscures interaction.

12. **Sound:** Washer cycles and belts; steam hiss telegraphed before cycle. Radio voices filtered behind office glass.

13. **Animation:** Adrian isolates press with lever, Noah removes loose lint screen and retrieves paper; hands stop before moving machinery. Mara inspects medical linen; Rusk folds clinic envelope into shirt. Contacts require authored alignment markers; no assumed animation availability.

14. **Complete dialogue:** Main sequence follows order below. Idle/retry lines only fire under named conditions; they are not spoken during canonical forward progress.



[CH01_M03_DLG001] MARA (natural, understated; 5.7s; main sequence): "Medical linen on the blue table. Keep it clear of the general wash."



[CH01_M03_DLG002] NOAH (intimate, tense; 4.1s; main sequence): "You are the doctor. Why are you counting sheets?"



[CH01_M03_DLG003] MARA (natural, understated; 4.9s; main sequence): "Because blood does not stop being evidence when somebody washes it."



[CH01_M03_DLG004] RUSK (clipped, guarded; 2.1s; main sequence): "Inspection, Doctor. Not conversation."



[CH01_M03_DLG005] ADRIAN (low, controlled; 4.1s; main sequence): "This press is catching. We need the inspection lamp."



[CH01_M03_DLG006] RUSK (clipped, guarded; 3.3s; main sequence): "You have one cycle. Then it works."



[CH01_M03_DLG007] ADRIAN (low, controlled; 4.1s; main sequence): "Lever down. Tell me when your hands are clear."



[CH01_M03_DLG008] NOAH (intimate, tense; 2.1s; main sequence): "Clear. Hold it there."



[CH01_M03_DLG009] NOAH (intimate, tense; 3.3s; main sequence): "There is a plan behind the screen."



[CH01_M03_DLG010] ADRIAN (low, controlled; 3.7s; main sequence): "Service corridor E. It runs behind our landing."



[CH01_M03_DLG011] NOAH (intimate, tense; 4.5s; main sequence): "Two relays. One opens the grille, one feeds the lock."



[CH01_M03_DLG012] ADRIAN (low, controlled; 2.0s; main sequence): "Same time?"



[CH01_M03_DLG013] NOAH (intimate, tense; 2.1s; main sequence): "Same circuit. Different rooms."



[CH01_M03_DLG014] MARA (natural, understated; 3.7s; main sequence): "Put the screen back before you restart it."



[CH01_M03_DLG015] RUSK (clipped, guarded; 2.1s; main sequence): "Doctor. The clinic called?"



[CH01_M03_DLG016] MARA (natural, understated; 4.1s; main sequence): "The envelope is sealed, Officer. Read it somewhere private."



[CH01_M03_DLG017] NOAH (intimate, tense; 2.0s; main sequence): "He looks frightened."



[CH01_M03_DLG018] ADRIAN (low, controlled; 3.7s; main sequence): "Remember that. Do not mistake it for kindness."



[CH01_M03_DLG019] ADRIAN (low, controlled; 4.5s; main sequence): "After count, I open my panel. You watch the landing."



[CH01_M03_DLG020] NOAH (intimate, tense; 4.5s; main sequence): "We leave together. No doors shut behind the other man."



[CH01_M03_DLG021] ADRIAN (low, controlled; 2.0s; main sequence): "Agreed."



[CH01_M03_DLG022] NOAH (intimate, tense; 2.0s; main sequence): "That sounded rehearsed."



[CH01_M03_DLG023] ADRIAN (low, controlled; 3.3s; main sequence): "It is a promise. Those need practice."



[CH01_M03_DLG024] NOAH (intimate, tense; 2.9s; lever released early): "Hands back. Lock it down again."



[CH01_M03_DLG025] RUSK (clipped, guarded; 2.1s; idle bark): "Less talking. More linen."



15. **Player actions and stage direction:** Mara asks for contaminated linen isolation. P2 deliberately starts the doctor conversation at the blue table (DLG003); Rusk turns to interrupt (DLG004), then goes to the office for the requested inspection lamp after DLG006. This is the nonviolent guard distraction. P1 locks out idle press lever while P2 clears screen, then P2 holds inspection lamp while P1 reads maintenance diagram. They restore screen before Rusk return. P2 palms discarded spring strip from scrap bin as shim.

16. **Cooperative mechanics:** Two-stage interlock: operator must keep isolation lever held; releasing pauses retrieval with hand withdrawn first. Diagram has north route on P1 view, relay key on P2 view, requiring spoken exchange.

17. **Objectives and triggers:** OBJ001 isolate and inspect; OBJ002 both inspect diagram halves; OBJ003 replace screen and collect shim. CS01 begins after Rusk leaves aisle. IDs are CH01_M03_OBJ001 onward in listed order. Checkpoint CP03_A at scene entry, CP03_B after final reversible puzzle; checkpoint restores both players, props, patrol phase and dialogue consumed flags atomically. No checkpoint inside locked cinematic.

18. **Transitions:** Main cinematic CH01_M03_CS01, divided into shots in the camera sheet. Opening shot may establish space, dialogue is spread across authored interactions as assigned below; never cram all dialogue into cinematic allocation. End fades only where camera sheet calls one. Completion grants next mission together; cancellation/reload restores pre-trigger state.

19. **Required assets:** CHAR_ADRIAN, CHAR_NOAH, CHAR_RUSK, CHAR_MARA, CHAR_GUARD, PROP_DIAGRAM, PROP_SHIM, PROP_RELAY, AUDIO_PRISON, ANIM_HUMANOID, MAT_CONCRETE, MAT_METAL, UI_SUBTITLES. These are requirements, not a claim that files exist. Every performance needs the appropriate clip in ANIM_HUMANOID; missing clips are blockers for final production.

20. **Ending state:** Diagram memorized, original returned to prevent suspicion. Shim concealed. Plan: cell service panel, restricted corridor, maintenance spillway door.



**Dialogue staging:** DLG001–006 assignment;007–009 press isolation;010–013 diagram read;014screenreplacement;015–016 clinic envelope;017–018 aside after Rusk leaves;019–023 escape pact. Optional idle/retry lines fire only under their named condition. Plot dialogue waits for hearing distance and preceding line completion.






## CH01_M04_SC01 — LIGHTS OUT



1. **Scene ID:** CH01_M04_SC01; principal cutscene CH01_M04_CS01.

2. **Title:** LIGHTS OUT.

3. **Location:** East cells and restricted service corridor. See mission [M04](../missions/CH01_MISSION_04.md).

4. **Time:** 18 October 2028, 22:10. One continuous day; no unexplained time jump within scene.

5. **Duration:** 360s total; 35s cinematic allocation, 325s playable estimate.

6. **Present:** RUSK, NOAH, ADRIAN, GUARD; two silent holding-bay inmates. Recording in M05 is an unidentified cached voice, not proof of Elena's current location.

7. **Purpose:** Turn verbal trust into coordinated risk; establish guards can hear footsteps without a supernatural alert.

8. **Environment:** ENV_CELLBLOCK, ENV_MAINTENANCE. Required readable routes, accessible interaction marks and camera clearance; see environment build specifications.

9. **Starting positions:** Adrian at cell13 rear panel (0,0,0); Noah at cell14 bars (3,0,0). Patrol guard starts west end landing (-8,0,3).

10. **Camera:** Begin with shot CH01_M04_CS01_SH01, then third-person P1/P2. See [shot list](CH01_CAMERA_SHOTS.md). Gameplay camera at 1.6m height, 2.8m trailing, collision retracts to 0.45m; interior gate framing must retain partner visibility.

11. **Lighting:** Night strips at reduced intensity; moving guard flashlight has visible cone; service exit has dim amber practical.

12. **Sound:** Count bell, boots and radio click; pipes carry whispered voice. Score remains low enough for patrol cue.

13. **Animation:** Shim panel, careful crouch through service opening, brace panel for partner, lean behind pier. No animation requires protagonists clipping through bars. Contacts require authored alignment markers; no assumed animation availability.

14. **Complete dialogue:** Main sequence follows order below. Idle/retry lines only fire under named conditions; they are not spoken during canonical forward progress.



[CH01_M04_DLG001] RUSK (clipped, guarded; 2.9s; main sequence): "Final count. Faces at the bars."



[CH01_M04_DLG002] NOAH (intimate, tense; 2.0s; main sequence): "Here."



[CH01_M04_DLG003] ADRIAN (low, controlled; 2.0s; main sequence): "Here."



[CH01_M04_DLG004] GUARD (clipped, guarded; 2.0s; main sequence): "East landing clear."



[CH01_M04_DLG005] NOAH (intimate, tense; 2.9s; main sequence): "He turns at the clock. Wait."



[CH01_M04_DLG006] ADRIAN (low, controlled; 2.0s; main sequence): "I am waiting."



[CH01_M04_DLG007] NOAH (intimate, tense; 2.9s; main sequence): "Now. His back is to us."



[CH01_M04_DLG008] ADRIAN (low, controlled; 3.7s; main sequence): "Panel is loose. Do not touch the edge."



[CH01_M04_DLG009] NOAH (intimate, tense; 3.3s; main sequence): "That is your idea of a door?"



[CH01_M04_DLG010] ADRIAN (low, controlled; 2.0s; main sequence): "Tonight it is."



[CH01_M04_DLG011] ADRIAN (low, controlled; 2.9s; main sequence): "Your hatch is open. Come through."



[CH01_M04_DLG012] NOAH (intimate, tense; 2.5s; main sequence): "Holding it. Move past me."



[CH01_M04_DLG013] GUARD (clipped, guarded; 2.0s; main sequence): "Who is there?"



[CH01_M04_DLG014] NOAH (intimate, tense; 2.1s; main sequence): "Stay behind the pier."



[CH01_M04_DLG015] ADRIAN (low, controlled; 3.3s; main sequence): "He heard the pipe. Let him pass."



[CH01_M04_DLG016] NOAH (intimate, tense; 2.5s; main sequence): "How far to the outside?"



[CH01_M04_DLG017] ADRIAN (low, controlled; 3.7s; main sequence): "Far enough that we keep our voices down."



[CH01_M04_DLG018] NOAH (intimate, tense; 2.9s; main sequence): "We still have the same promise?"



[CH01_M04_DLG019] ADRIAN (low, controlled; 2.5s; main sequence): "We still have two people."



[CH01_M04_DLG020] GUARD (clipped, guarded; 2.5s; detected fail only): "Stop! Hands above your head!"



[CH01_M04_DLG021] NOAH (intimate, tense; 2.9s; retry CP04_A): "Wait for his turn this time."



[CH01_M04_DLG022] ADRIAN (low, controlled; 2.5s; patrol warning): "Hold. Boots on the landing."



15. **Player actions and stage direction:** P2 calls patrol turn from bars. P1 shims rear fastener and enters common service chase, unlatching cell14 service hatch from rear. P2 follows and holds hatch while P1 clears it. Alternate movement between concrete piers; reach restricted corridor manual gate.

16. **Cooperative mechanics:** P1 cannot observe landing while shimming. P2 must call turn; ready prompt can wait indefinitely. Both physically clear hatch before either may close it.

17. **Objectives and triggers:** OBJ001 open two rear panels; OBJ002 both cross chase; OBJ003 reach gate unseen. CS01 at gate. Detection triggers fail overlay and reload CP04_A, never canonical capture. IDs are CH01_M04_OBJ001 onward in listed order. Checkpoint CP04_A at scene entry, CP04_B after final reversible puzzle; checkpoint restores both players, props, patrol phase and dialogue consumed flags atomically. No checkpoint inside locked cinematic.

18. **Transitions:** Main cinematic CH01_M04_CS01, divided into shots in the camera sheet. Opening shot may establish space, dialogue is spread across authored interactions as assigned below; never cram all dialogue into cinematic allocation. End fades only where camera sheet calls one. Completion grants next mission together; cancellation/reload restores pre-trigger state.

19. **Required assets:** CHAR_ADRIAN, CHAR_NOAH, CHAR_RUSK, CHAR_GUARD, PROP_SHIM, AUDIO_PRISON, ANIM_HUMANOID, MAT_CONCRETE, MAT_METAL, UI_SUBTITLES. These are requirements, not a claim that files exist. Every performance needs the appropriate clip in ANIM_HUMANOID; missing clips are blockers for final production.

20. **Ending state:** Both beyond cell chase at locked maintenance gate. Panels returned flush; guard has not found empty cells.



**Dialogue staging:** DLG001–004 count;005–007 lookout/shim;008–012 hatch traverse;013guardambiguouspipeinvestigation (not fail);014–015 hide behind pier;016–019 gate conversation. Separate detected bark only on hard detection. Optional idle/retry lines fire only under their named condition. Plot dialogue waits for hearing distance and preceding line completion.






## CH01_M05_SC01 — BEHIND THE WALLS



1. **Scene ID:** CH01_M05_SC01; principal cutscene CH01_M05_CS01.

2. **Title:** BEHIND THE WALLS.

3. **Location:** Maintenance relay rooms and pump hall. See mission [M05](../missions/CH01_MISSION_05.md).

4. **Time:** 18 October 2028, 22:24. One continuous day; no unexplained time jump within scene.

5. **Duration:** 420s total; 65s cinematic allocation, 355s playable estimate.

6. **Present:** ADRIAN, NOAH, RECORDING. Recording in M05 is an unidentified cached voice, not proof of Elena's current location.

7. **Purpose:** Make dependence physical; introduce an uncertain recent voice clue and evidence of prisoner transfer.

8. **Environment:** ENV_MAINTENANCE. Required readable routes, accessible interaction marks and camera clearance; see environment build specifications.

9. **Starting positions:** Adrian at west relay access (0,0,0); Noah at east crawl gate (4,0,0). Routes rejoin pump hall (2,0,-16).

10. **Camera:** Begin with shot CH01_M05_CS01_SH01, then third-person P1/P2. See [shot list](CH01_CAMERA_SHOTS.md). Gameplay camera at 1.6m height, 2.8m trailing, collision retracts to 0.45m; interior gate framing must retain partner visibility.

11. **Lighting:** Amber lamps and readable relay faceplates; moving pump shadows, no strobing.

12. **Sound:** Pump pulse; insulated room muffles partner; maintenance handset provides communication. Recording is distorted but intelligible with subtitles marked recording.

13. **Animation:** P1 turns isolated selector; P2 holds mechanical brake; both pull separate door handles; Noah freezes at voice then deliberately lowers handset. Contacts require authored alignment markers; no assumed animation availability.

14. **Complete dialogue:** Main sequence follows order below. Idle/retry lines only fire under named conditions; they are not spoken during canonical forward progress.



[CH01_M05_DLG001] ADRIAN (low, controlled; 2.9s; main sequence): "West side is a catwalk. Yours?"



[CH01_M05_DLG002] NOAH (intimate, tense; 3.7s; main sequence): "Floor route. Water below it, no way across."



[CH01_M05_DLG003] ADRIAN (low, controlled; 2.1s; main sequence): "Take the handset. Test."



[CH01_M05_DLG004] NOAH (intimate, tense; 3.7s; main sequence): "I hear you. Better than through a wall."



[CH01_M05_DLG005] ADRIAN (low, controlled; 4.1s; main sequence): "Selector has A, B, C. Which feeds the grille?"



[CH01_M05_DLG006] NOAH (intimate, tense; 4.1s; main sequence): "Diagram said B. Brake first. Give me a second."



[CH01_M05_DLG007] NOAH (intimate, tense; 4.1s; main sequence): "Brake held. My hands are clear of the chain."



[CH01_M05_DLG008] ADRIAN (low, controlled; 2.1s; main sequence): "Selecting B. Power on."



[CH01_M05_DLG009] NOAH (intimate, tense; 4.1s; main sequence): "Grille is up. Latch caught. You can let go."



[CH01_M05_DLG010] ADRIAN (low, controlled; 2.5s; main sequence): "Meet me by the pump."



[CH01_M05_DLG011] NOAH (intimate, tense; 2.0s; main sequence): "You waited."



[CH01_M05_DLG012] ADRIAN (low, controlled; 2.1s; main sequence): "I said I would."



[CH01_M05_DLG013] ADRIAN (low, controlled; 4.5s; main sequence): "Look at the dates. Transfer codes. No names. No destination."



[CH01_M05_DLG014] NOAH (intimate, tense; 3.3s; main sequence): "A boat every Thursday. No receiving prison."



[CH01_M05_DLG015] RECORDING (natural, understated; 4.9s; main sequence): "Calibration log. Channel seven. Tell N the harbor light still turns."



[CH01_M05_DLG016] NOAH (intimate, tense; 2.0s; main sequence): "Play that again."



[CH01_M05_DLG017] ADRIAN (low, controlled; 4.5s; main sequence): "It is damaged. We do not know who that is."



[CH01_M05_DLG018] NOAH (intimate, tense; 4.5s; main sequence): "Elena said that when our father was late coming home."



[CH01_M05_DLG019] ADRIAN (low, controlled; 4.1s; main sequence): "Somebody could know that. A recording could be old."



[CH01_M05_DLG020] NOAH (intimate, tense; 2.1s; main sequence): "The console says yesterday."



[CH01_M05_DLG021] ADRIAN (low, controlled; 4.9s; main sequence): "That is when it was copied. Keep the words. Keep moving."



[CH01_M05_DLG022] NOAH (intimate, tense; 5.3s; main sequence): "If there is a boat, there is a way to find her."



[CH01_M05_DLG023] NOAH (intimate, tense; 3.3s; wrong selector): "Breaker tripped. Set it back to neutral."



[CH01_M05_DLG024] ADRIAN (low, controlled; 3.3s; puzzle retry): "No rush. Brake, then B, then power."



15. **Player actions and stage direction:** Open gate with shim. P1 takes west catwalk, P2 east floor route. Read selector labels and brake status across wired maintenance handsets. P2 holds brake, P1 sets selector B then energizes only after clear call. Grille rises; both release controls and reunite through mechanically latched gate. Inspect transfer ledger and cached diagnostic recording at pump console. Approach spillway door together.

16. **Cooperative mechanics:** Stable puzzle, no lethal electrical handling: closed labeled switchgear only. Wrong selector trips safe breaker and resets state. Handsets substitute for impossible room acoustics. Both routes have independent return access.

17. **Objectives and triggers:** OBJ001 reach relays; OBJ002 correct selector plus brake; OBJ003 both reunite; OBJ004 inspect ledger and voice; OBJ005 both approach door. CS01 plays console clue then returns control. IDs are CH01_M05_OBJ001 onward in listed order. Checkpoint CP05_A at scene entry, CP05_B after final reversible puzzle; checkpoint restores both players, props, patrol phase and dialogue consumed flags atomically. No checkpoint inside locked cinematic.

18. **Transitions:** Main cinematic CH01_M05_CS01, divided into shots in the camera sheet. Opening shot may establish space, dialogue is spread across authored interactions as assigned below; never cram all dialogue into cinematic allocation. End fades only where camera sheet calls one. Completion grants next mission together; cancellation/reload restores pre-trigger state.

19. **Required assets:** CHAR_ADRIAN, CHAR_NOAH, PROP_RELAY, PROP_LEDGER, AUDIO_PRISON, ANIM_HUMANOID, MAT_CONCRETE, MAT_METAL, UI_SUBTITLES. These are requirements, not a claim that files exist. Every performance needs the appropriate clip in ANIM_HUMANOID; missing clips are blockers for final production.

20. **Ending state:** Partial pump service ledger shows coded recurring offshore transfers, with no names or destination; the full rendition ledger is a distinct CH06 discovery. This ledger shows recurring offshore transfers; Noah suspects Elena survived but has no confirmation. They reach final door with incomplete evidence.



**Dialogue staging:** DLG001–004 route split and handsets;005–009 relay/brake puzzle;010traverse;011–012 reunion;013–014 ledger inspection;015 recording;016–021 console reaction;022 door approach. Optional idle/retry lines fire only under their named condition. Plot dialogue waits for hearing distance and preceding line completion.






## CH01_M06_SC01 — THE BETRAYAL



1. **Scene ID:** CH01_M06_SC01; principal cutscene CH01_M06_CS01.

2. **Title:** THE BETRAYAL.

3. **Location:** Spillway security door, holding corridor and solitary. See mission [M06](../missions/CH01_MISSION_06.md).

4. **Time:** 18 October 2028, 22:36. One continuous day; no unexplained time jump within scene.

5. **Duration:** 270s total; 100s cinematic allocation, 170s playable estimate.

6. **Present:** NOAH, ADRIAN, RUSK, two GUARD officers. Recording in M05 is an unidentified cached voice, not proof of Elena's current location.

7. **Purpose:** Defeat the escape without invalidating cooperation; reveal Rusk as informant, preserve his coercion mystery and seed Chapter2.

8. **Environment:** ENV_MAINTENANCE, ENV_CELLBLOCK. Required readable routes, accessible interaction marks and camera clearance; see environment build specifications.

9. **Starting positions:** Adrian west handle (-1,0,0); Noah east handle (1,0,0). Rusk and two guards concealed beyond security grille (0,0,-6).

10. **Camera:** Begin with shot CH01_M06_CS01_SH01, then third-person P1/P2. See [shot list](CH01_CAMERA_SHOTS.md). Gameplay camera at 1.6m height, 2.8m trailing, collision retracts to 0.45m; interior gate framing must retain partner visibility.

11. **Lighting:** Amber spillway practical changes to steady red alarm wash; no rapid flashing. Solitary overhead pools separated by black wall.

12. **Sound:** Door mechanism, alarm, weapons raised but no shots. Alarm ducks under dialogue. Pipe knocks close chapter.

13. **Animation:** Both pull handles; Rusk raises palm, guards aim low ready then restrain after protagonists surrender. Noah attempts step forward, Adrian stops him with forearm. Controlled cuff and kneel animations; no player struggle QTE. Contacts require authored alignment markers; no assumed animation availability.

14. **Complete dialogue:** Main sequence follows order below. Idle/retry lines only fire under named conditions; they are not spoken during canonical forward progress.



[CH01_M06_DLG001] NOAH (intimate, tense; 2.1s; main sequence): "Two handles. One promise."



[CH01_M06_DLG002] ADRIAN (low, controlled; 2.5s; main sequence): "On three. One. Two. Three."



[CH01_M06_DLG003] RUSK (clipped, guarded; 2.9s; main sequence): "Let go of the door. Slowly."



[CH01_M06_DLG004] NOAH (intimate, tense; 2.0s; main sequence): "You followed us."



[CH01_M06_DLG005] RUSK (clipped, guarded; 2.9s; main sequence): "I was told where to wait."



[CH01_M06_DLG006] ADRIAN (low, controlled; 4.1s; main sequence): "You left the diagram where we could find it."



[CH01_M06_DLG007] RUSK (clipped, guarded; 5.3s; main sequence): "I left you a route. I thought that was all they wanted."



[CH01_M06_DLG008] NOAH (intimate, tense; 2.0s; main sequence): "Who are they?"



[CH01_M06_DLG009] RUSK (clipped, guarded; 2.1s; main sequence): "Hands on your heads."



[CH01_M06_DLG010] NOAH (intimate, tense; 2.5s; main sequence): "That voice. Was it her?"



[CH01_M06_DLG011] RUSK (clipped, guarded; 2.1s; main sequence): "I do not know."



[CH01_M06_DLG012] ADRIAN (low, controlled; 3.7s; main sequence): "Then look at him when you say it."



[CH01_M06_DLG013] RUSK (clipped, guarded; 2.1s; main sequence): "I do not know."



[CH01_M06_DLG014] GUARD (clipped, guarded; 2.9s; main sequence): "On your knees. Both of you."



[CH01_M06_DLG015] NOAH (intimate, tense; 2.1s; main sequence): "We can still run."



[CH01_M06_DLG016] ADRIAN (low, controlled; 3.3s; main sequence): "No. Look at me. We stay alive."



[CH01_M06_DLG017] NOAH (intimate, tense; 2.5s; main sequence): "You knew this could happen."



[CH01_M06_DLG018] ADRIAN (low, controlled; 5.3s; main sequence): "I knew nothing was free. I did not know it was him."



[CH01_M06_DLG019] RUSK (clipped, guarded; 3.7s; main sequence): "Separate cells. No hospital transfer. They stay here."



[CH01_M06_DLG020] GUARD (clipped, guarded; 2.5s; main sequence): "That is not your decision."



[CH01_M06_DLG021] RUSK (clipped, guarded; 2.5s; main sequence): "Write my name on it."



[CH01_M06_DLG022] NOAH (intimate, tense; 2.0s; main sequence): "Cross?"



[CH01_M06_DLG023] ADRIAN (low, controlled; 2.0s; main sequence): "Still here."



[CH01_M06_DLG024] NOAH (intimate, tense; 2.0s; main sequence): "The harbor light."



[CH01_M06_DLG025] ADRIAN (low, controlled; 2.0s; main sequence): "Still turns."



[CH01_M06_DLG026] NOAH (intimate, tense; 2.5s; main sequence): "Then we try another way."



[CH01_M06_DLG027] ADRIAN (low, controlled; 3.3s; handle idle): "Together. I am ready when you are."



[CH01_M06_DLG028] NOAH (intimate, tense; 3.3s; pipe idle): "Three knocks. If you can hear me."



15. **Player actions and stage direction:** Both inspect lock and pull handles. Security grille closes behind on CS01 trigger; no false escape skill test. Players retain look during reveal but no movement. After fade, P1 then P2 independently interact with solitary pipe; three knocks and response complete chapter.

16. **Cooperative mechanics:** Final handle action requires both ready. Capture is authored canonical event, not a failure. Solitary pipe sequence gives both players an active closing response.

17. **Objectives and triggers:** OBJ001 both pull handles; CS01 alarm and capture; OBJ002 both answer pipe. End card CH02 NIGHT SHIFT only after both interactions. IDs are CH01_M06_OBJ001 onward in listed order. Checkpoint CP06_A at scene entry, CP06_B after final reversible puzzle; checkpoint restores both players, props, patrol phase and dialogue consumed flags atomically. No checkpoint inside locked cinematic.

18. **Transitions:** Main cinematic CH01_M06_CS01, divided into shots in the camera sheet. Opening shot may establish space, dialogue is spread across authored interactions as assigned below; never cram all dialogue into cinematic allocation. End fades only where camera sheet calls one. Completion grants next mission together; cancellation/reload restores pre-trigger state.

19. **Required assets:** CHAR_ADRIAN, CHAR_NOAH, CHAR_RUSK, CHAR_GUARD, PROP_SHIM, PROP_LEDGER, AUDIO_PRISON, ANIM_HUMANOID, MAT_CONCRETE, MAT_METAL, UI_SUBTITLES, VFX_ALARM. These are requirements, not a claim that files exist. Every performance needs the appropriate clip in ANIM_HUMANOID; missing clips are blockers for final production.

20. **Ending state:** Both alive, separately confined; shim confiscated; approved photograph remains in Noah's shirt after routine restraint search, other intake property remains locker42; ledger remains at pump console. No carried evidence. Noah retains phrase and transfer schedule in memory. Rusk betrayal known, daughter coercion not yet confirmed.



**Dialogue staging:** DLG001–002 playable dualhandle ready;003–021 uninterrupted capture cinematic;022–026 solitary playable pipe response, after three knocks. No dialogue choices during capture. Optional idle/retry lines fire only under their named condition. Plot dialogue waits for hearing distance and preceding line completion.





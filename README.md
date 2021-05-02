# ticket_bot_example
[This code is ticket bot exmple]
This code has three events
First is on_message for commend to make ticket channel
Second is on_raw_reaction_add for add emoji to make ticket channel
(I use on_raw_reaction_add (not on_reaction_add). This is because on_raw_reaction_add can see the emoji addition of uncached messages.)
Third is on_error for debugging

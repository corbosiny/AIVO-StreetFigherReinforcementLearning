previous_enemy_health = 175
previous_enemy_matches_won = 0

previous_score = 0
previous_health = 175
previous_matches_won = 0

function calculate_reward()
  reward = 0
  
  --if data.score > previous_score then
  --  local delta = data.score - previous_score
  --  previous_score = data.score
  --  reward = reward + delta
  --end  
  
  if data.health < previous_health then
    local delta = data.health - previous_health
    previous_health = data.health
    reward = reward + delta
  end
  
  if data.enemy_health < previous_enemy_health then
    local delta = previous_enemy_health - data.enemy_health
    previous_enemy_health = data.enemy_health
    reward = reward + delta
  end
  
  if data.matches_won > previous_matches_won then
    local delta = 100
    previous_matches_won = data.matches_won
    reward = reward + delta
  end
  
  if data.enemy_matches_won > previous_enemy_matches_won then
    local delta = -100
    previous_enemy_matches_won = data.enemy_matches_won
    reward = reward + delta
  end
  
  return reward
  
end

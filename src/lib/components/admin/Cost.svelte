<script>
  import { onMount } from 'svelte';
  import { getCostData, createCostRecord, updateCostRecord } from '$lib/apis/costs';
  import { user } from '$lib/stores';
  import { goto } from '$app/navigation';

  let costData = [];
  let groupedByUser = [];
  let groupedByGroup = [];
  let groupedByModel = [];

  const groupData = (data, key) => {
    return data.reduce((result, item) => {
      (result[item[key]] = result[item[key]] || []).push(item);
      return result;
    }, {});
  };

  const handleCreateCost = async () => {
    const newCost = {
      user_id: 'new_user_id',
      group_id: 'new_group_id',
      model_id: 'new_model_id',
      input_tokens: 100,
      output_tokens: 200,
      cost: 50.0
    };
    await createCostRecord(localStorage.token, newCost);
    costData = await getCostData(localStorage.token);
    groupedByUser = groupData(costData, 'user_id');
    groupedByGroup = groupData(costData, 'group_id');
    groupedByModel = groupData(costData, 'model_id');
  };

  const handleUpdateCost = async (costId) => {
    const updatedCost = {
      input_tokens: 150,
      output_tokens: 250,
      cost: 75.0
    };
    await updateCostRecord(localStorage.token, costId, updatedCost);
    costData = await getCostData(localStorage.token);
    groupedByUser = groupData(costData, 'user_id');
    groupedByGroup = groupData(costData, 'group_id');
    groupedByModel = groupData(costData, 'model_id');
  };

  onMount(async () => {
    if ($user?.role !== 'admin') {
      await goto('/');
    } else {
      costData = await getCostData(localStorage.token);
      groupedByUser = groupData(costData, 'user_id');
      groupedByGroup = groupData(costData, 'group_id');
      groupedByModel = groupData(costData, 'model_id');
    }
  });
</script>

<div class="cost-analysis">
  <h1>Cost Analysis</h1>

  <div class="grouped-data">
    <h2>Grouped by User</h2>
    {#each Object.keys(groupedByUser) as userId}
      <div class="user-group">
        <h3>User ID: {userId}</h3>
        <ul>
          {#each groupedByUser[userId] as cost}
            <li>Model: {cost.model_id}, Input Tokens: {cost.input_tokens}, Output Tokens: {cost.output_tokens}, Cost: {cost.cost}</li>
            <button on:click={() => handleUpdateCost(cost.id)}>Update Cost</button>
          {/each}
        </ul>
      </div>
    {/each}
  </div>

  <div class="grouped-data">
    <h2>Grouped by Group</h2>
    {#each Object.keys(groupedByGroup) as groupId}
      <div class="group-group">
        <h3>Group ID: {groupId}</h3>
        <ul>
          {#each groupedByGroup[groupId] as cost}
            <li>User: {cost.user_id}, Model: {cost.model_id}, Input Tokens: {cost.input_tokens}, Output Tokens: {cost.output_tokens}, Cost: {cost.cost}</li>
            <button on:click={() => handleUpdateCost(cost.id)}>Update Cost</button>
          {/each}
        </ul>
      </div>
    {/each}
  </div>

  <div class="grouped-data">
    <h2>Grouped by Model</h2>
    {#each Object.keys(groupedByModel) as modelId}
      <div class="model-group">
        <h3>Model ID: {modelId}</h3>
        <ul>
          {#each groupedByModel[modelId] as cost}
            <li>User: {cost.user_id}, Group: {cost.group_id}, Input Tokens: {cost.input_tokens}, Output Tokens: {cost.output_tokens}, Cost: {cost.cost}</li>
            <button on:click={() => handleUpdateCost(cost.id)}>Update Cost</button>
          {/each}
        </ul>
      </div>
    {/each}
  </div>

  <button on:click={handleCreateCost}>Create New Cost</button>
</div>

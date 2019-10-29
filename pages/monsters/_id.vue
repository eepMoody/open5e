<template>
  <section class="container docs-container"> 
    <p v-if="loading"> Loading... </p>
    <div v-else>
      <h1>{{monster.name}}</h1>
      <img v-if="monster.img_main" :src="monster.img_main" class="img-main">
      <p><em>{{monster.size}} {{monster.type}}, {{monster.alignment}}</em></p>
      <hr/>
      <p> <b>Armor Class</b> {{monster.armor_class}}</p>
      <p> <b>Hit Points</b> {{monster.hit_points}} ({{monster.hit_dice}})</p>
      <p> <b>Speed</b>
      <span v-for="(speed, key, index) in monster.speed" :key="index" v-if="key !== 'hover'">
        {{key.charAt(0).toUpperCase() + key.slice(1)}} {{speed}}ft. 
        <span v-if="monster.speed.hasOwnProperty('hover') && key === 'fly'">(hover)</span>
      </span>
      </p>
      <hr/>
      <div class="ability-array">
        <div class="ability-block">
          <span class="ability-name">STR</span>
          <span class="ability-score">{{monster.strength}} (<stat-bonus :stat="monster.strength"></stat-bonus>)</span> 
          
        </div> 
        <div class="ability-block">
          <span class="ability-name">DEX</span>
          <span class="ability-score">{{monster.dexterity}} (<stat-bonus :stat="monster.dexterity"></stat-bonus>)</span> 
          
        </div> 
        <div class="ability-block">
          <span class="ability-name">CON</span>
          <span class="ability-score">{{monster.constitution}} (<stat-bonus :stat="monster.constitution"></stat-bonus>)</span> 
          
        </div> 
        <div class="ability-block">
          <span class="ability-name">INT</span>
          <span class="ability-score">{{monster.intelligence}} (<stat-bonus :stat="monster.intelligence"></stat-bonus>)</span> 
          
        </div> 
        <div class="ability-block">
          <span class="ability-name">WIS</span>
          <span class="ability-score">{{monster.wisdom}} (<stat-bonus :stat="monster.wisdom"></stat-bonus>)</span> 
          
        </div>
        <div class="ability-block">
          <span class="ability-name">CHA</span>
          <span class="ability-score">{{monster.charisma}} (<stat-bonus :stat="monster.charisma"></stat-bonus>)</span> 
          
        </div>
      </div>
      <hr/>
      <p v-if="getSaves">
        <b>Saving Throws</b>
        <span v-for="(save, index) in getSaves" :key="save.name">
          {{save.name}}
          <stat-bonus :stat="save.val" :type="save.type"></stat-bonus><span v-if="index < getSaves.length -1">, </span>
        </span>
      </p>
      <p v-if="monster.skills"> 
        <b>Skills</b>
        <span v-for="(skill, key, index) in monster.skills" :key="index" v-if="key !== 'hover'">
        {{key.charAt(0).toUpperCase() + key.slice(1)}}
        <span v-if="skill >=0 ">+</span>{{skill}}<span v-if="index < getSaves.length -1">, </span>
        </span>
      </p>
      <p v-if="monster.damage_vulnerabilities"> <b>Damage Vulnerabilities</b> {{monster.damage_vulnerabilities}} </p>
      <p v-if="monster.damage_resistances"> <b>Damage Resistances</b> {{monster.damage_resistances}} </p>
      <p v-if="monster.damage_immunities"> <b>Damage Immunities</b> {{monster.damage_immunities}} </p>
      <p v-if="monster.senses"> <b>Senses</b> {{monster.senses}} </p>
      <p v-if="monster.languages"> <b>Languages</b> {{monster.languages}} </p>
      <p v-if="monster.challenge_rating"> <b>Challenge</b> <challenge-render :challenge="monster.challenge_rating"></challenge-render> </p>
      <hr/>
      <p class="action-block" v-for="ability in monster.special_abilities" v-bind:key="ability.name">
        <b class="action-name">{{ability.name}}. </b> <md-viewer class="inline" :text="ability.desc"></md-viewer>
      </p>
      <h2 v-if="monster.actions">Actions</h2>
      <p class="action-block" v-for="action in monster.actions" v-bind:key="action.name">
        <b class="action-name">{{action.name}}. </b> <md-viewer class="inline" :text="action.desc"></md-viewer>
      </p>
      <h2 v-if="monster.reactions">Reactions</h2>
      <p class="action-block" v-for="action in monster.reactions" v-bind:key="action.name">
        <b class="action-name">{{action.name}}. </b> <md-viewer class="inline" :text="action.desc"></md-viewer>
      </p>
      <h2 v-if="monster.legendary_actions">Legendary Actions</h2>
      <p class="action-block" v-for="action in monster.legendary_actions" v-bind:key="action.name">
        <b class="action-name">{{action.name}}. </b> <md-viewer class='inline' :text="action.desc"></md-viewer>
      </p>
    </div>
    <p v-if="spells.length">
      <collapse>
        <button slot="collapse-header">
            Show associated spells
        </button>
        <div slot="collapse-body" class="spell-cards">
          <div v-for="spell in spells" class="spell-card" v-bind:key="spell.slug">
            <h4>{{spell.name}}</h4>
            <p><em>{{spell.level}} {{spell.school}}</em> | {{spell.dnd_class}}</p>
            <p><b>Range:</b> {{spell.range}}</p>
            <p><b>Casting Time:</b> {{spell.casting_time}} <span v-if="spell.ritual === 'yes'">{{spell.ritual}} (Ritual)</span></p>
            <p><b>Duration:</b> {{spell.duration}} <span v-if="spell.concentration === 'yes'">(Concentration)</span></p>
            <p><b>Components: {{spell.components}} <span v-if="spell.material">({{spell.material}})</span></b></p>
            <md-viewer :text="spell.desc"></md-viewer>
            <p v-if="spell.higher_level"><b>At higher levels:</b> {{spell.higher_level}}</p>
          </div>
        </div>
      </collapse>

    </p>
  </section>
</template>

<script>
import axios from 'axios';
import StatBonus from '~/components/StatBonus.vue';
import ChallengeRender from '~/components/ChallengeRender.vue';
import MdViewer from '~/components/MdViewer';
import Collapse from '~/components/Collapse'

export default {
  components: {
    StatBonus,
    ChallengeRender,
    MdViewer,
    Collapse,
  },
  created () {
    return axios.get(`${process.env.apiUrl}/monsters/${this.$route.params.id}`)
    .then(response => {
      this.monster = response.data;
      this.loading = false
      if (this.monster.spell_list.length > 0) {
        this.getSpellList(this.monster.spell_list);
      }
    })
  },
  computed: {
    getSaves() {
      let saves = [];
      let savesArray = [
        {name: 'strength', display: 'Str'}, 
        {name: 'dexterity', display: 'Dex'}, 
        {name: 'constitution', display: 'Con'}, 
        {name: 'intelligence', display: 'Int'}, 
        {name: 'wisdom', display: 'Wis'}, 
        {name: 'charisma', display: 'Cha'}
      ]
      // build an object of save bonuses if they exist
      for (let i = 0; i < savesArray.length; i++) {
        const saveValue = this.monster[savesArray[i].name + '_save'];
        const statValue = this.monster[savesArray[i].name];
        if (saveValue !== null) {
          saves.push({name: savesArray[i].display, val: saveValue, type: 'bonus'})
        } else {
          saves.push({name: savesArray[i].display, val: statValue, type: 'score'})
        }
      }  
      
      return saves;
    },
  },
  methods: {
    getSpellList: function(spell_list) {
      let spellNames = [];
      for (let i = 0; i < spell_list.length; i++) {
        let parts = spell_list[i].split("/")
        var lastSegment = parts.pop() || parts.pop();
        spellNames.push(lastSegment)
      }
      console.log(spellNames);
      return axios.get(`${process.env.apiUrl}/spells?slug__in=${spellNames}`)
      .then(response => {
        this.spells = response.data.results
      })
    }
  },
  data () {
    return {
      posts: [],
      errors: [],
      monster: [],
      spells: [],
      loading: true,
    }
  },
}
</script>

<style scoped lang="scss">
.img-main {
  float: right;
  width: 30%;
  min-width: 300px;
}

@media screen and (max-width: 600px) {
  .img-main {
    float: none;
    width: 100%;
  }
}

.action-block {

  .inline {
    display: inline;

    /deep/ p:first-child {
      display: inline;
    }
  }

  .action-name {
    font-size: 1.1rem;
  }
}

.ability-array {
  display: flex;
  flex-direction: row;
  justify-content: space-between; 
  max-width: 30rem;
  
  .ability-block {
    display: flex;
    flex-direction: column;
    align-items: center;
    
    .ability-name {
      font-weight: bold;
    }
  }
}
</style>


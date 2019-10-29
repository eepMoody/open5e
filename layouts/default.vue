<template>
  <div>
    <div class="app-wrapper" :class="{ 'show-sidebar': showSidebar }">
      <div class="sidebar">
        <nuxt-link tag="h1" to="/">Open5e</nuxt-link>
        <input class="input-search" 
          placeholder="Search Open5e"
          v-model="searchText" 
          v-on:keyup.enter="doSearch(searchText)">
        <ul v-if="sections && races && classes">
          <!-- Characters -->
          <nuxt-link tag="li" to="/characters/">Characters</nuxt-link>
          <ul v-show="$nuxt.$route.path.indexOf('/characters') != -1 || containsAnyString(charSections)">
            <nuxt-link v-for="section in charSections" v-bind:key="section.slug" tag="li" :to="`/sections/${section.slug}`">
              {{section.name}}
            </nuxt-link>
          </ul>
          <!-- Classes -->
          <nuxt-link tag="li" to="/classes">Classes</nuxt-link>
          <ul v-show="$nuxt.$route.path.indexOf('/classes') != -1">
            <nuxt-link v-for="charClass in classes" v-bind:key="charClass.slug" tag="li" :to="`/classes/${charClass.slug}`">
              {{charClass.name}}
            </nuxt-link>
          </ul>
          <!-- Races -->
          <nuxt-link tag="li" to="/races">Races</nuxt-link>
          <ul v-if="races" v-show="$nuxt.$route.path.indexOf('/races') != -1">
            <nuxt-link v-for="race in races" v-bind:key="race.slug" tag="li" :to="`/races/${race.slug}`">
              {{race.name}}
            </nuxt-link>
          </ul>
          <!-- Combat -->  
          <nuxt-link tag="li" to="/combat/">Combat</nuxt-link>
          <ul v-show="$nuxt.$route.path.indexOf('/combat/') != -1">
            <nuxt-link tag="li" to="/combat/actions">Actions in Combat</nuxt-link>
            <nuxt-link tag="li" to="/combat/attacking">Attacking</nuxt-link>
            <nuxt-link tag="li" to="/combat/combat-sequence">Combat Sequence</nuxt-link>
            <nuxt-link tag="li" to="/combat/cover">Cover</nuxt-link>
            <nuxt-link tag="li" to="/combat/damage-and-healing">Damage &amp; Healing</nuxt-link>
            <nuxt-link tag="li" to="/combat/mounted-combat">Mounted combat</nuxt-link>
            <nuxt-link tag="li" to="/combat/movement-in-combat">Movement in Combat</nuxt-link>
            <nuxt-link tag="li" to="/combat/underwater-combat">Underwater Combat</nuxt-link>
          </ul>
          <!-- Equipment -->
          <nuxt-link tag="li" to="/sections/equipment/">Equipment</nuxt-link>
          <ul v-show="containsAnyString(sectionGroups.Equipment)">
            <nuxt-link tag="li" :to="`/sections/${section.slug}`" v-for="section in sectionGroups.Equipment" v-bind:key="section.slug">
              {{section.name}}
            </nuxt-link>
          </ul>
          <!-- Magic Items -->
          <nuxt-link tag="li" v-bind:class="{'nuxt-link-active': $nuxt.$route.path.indexOf('/magicitems') === 0}" to="/magicitems/magicitem-list">Magic Items</nuxt-link>
          <!-- Spells -->
          <nuxt-link tag="li" v-bind:class="{'nuxt-link-active': $nuxt.$route.path.indexOf('/spells') === 0}" to="/spells/spells-table">Spells</nuxt-link>
          <ul v-show="$nuxt.$route.path.indexOf('/spells/') !== -1">
            <nuxt-link tag="li" to="/spells/by-class/bard">Bard Spells</nuxt-link>
            <nuxt-link tag="li" to="/spells/by-class/cleric">Cleric Spells</nuxt-link>
            <nuxt-link tag="li" to="/spells/by-class/druid">Druid Spells</nuxt-link>
            <nuxt-link tag="li" to="/spells/by-class/paladin">Paladin Spells</nuxt-link>
            <nuxt-link tag="li" to="/spells/by-class/sorcerer">Sorcerer Spells</nuxt-link>
            <nuxt-link tag="li" to="/spells/by-class/wizard">Wizard Spells</nuxt-link>
            <nuxt-link tag="li" to="/spells/by-class/warlock">Warlock Spells</nuxt-link>
          </ul>
          <!-- Monsters -->
          <nuxt-link tag="li" v-bind:class="{'nuxt-link-active': $nuxt.$route.path.indexOf('/monsters') === 0}" to="/monsters/monster-list">Monsters</nuxt-link>
          <!-- Gameplay Mechanics -->
          <nuxt-link tag="li" to="/gameplay-mechanics/">Gameplay Mechanics</nuxt-link>
          <ul v-show="$nuxt.$route.path.indexOf('/gameplay-mechanics/') !== -1">
            <nuxt-link tag="li" to="/gameplay-mechanics/ability-scores">Ability Scores</nuxt-link>
            <nuxt-link tag="li" to="/gameplay-mechanics/between-adventures">Between Adventures</nuxt-link>
            <nuxt-link tag="li" to="/gameplay-mechanics/conditions">Conditions</nuxt-link>
            <nuxt-link tag="li" to="/gameplay-mechanics/environment">Environment</nuxt-link>
            <nuxt-link tag="li" to="/gameplay-mechanics/movement">Movement</nuxt-link>
            <nuxt-link tag="li" to="/gameplay-mechanics/rest">Rest</nuxt-link>
            <nuxt-link tag="li" to="/gameplay-mechanics/saving-throws">Saving Throws</nuxt-link>
            <nuxt-link tag="li" to="/gameplay-mechanics/time">Time</nuxt-link>
          </ul>
          <!-- Running a Game -->
          <nuxt-link tag="li" to="/running/">Appendixes</nuxt-link>
          <ul v-show="$nuxt.$route.path.indexOf('/running') != -1 || containsAnyString(sectionGroups.Characters)">
            <nuxt-link tag="li" :to="`/running/${section.slug}`" v-for="section in sectionGroups.Rules" v-bind:key="section.slug">
              {{section.name}}
            </nuxt-link>
          </ul>
          <nuxt-link tag="li" to="/api-docs">API Docs</nuxt-link>
        </ul>
        <a class="sidebar-link" href="https://www.patreon.com/open5e"><img src="/img/patron-badge.png" class="sidebar-image"></a>
      </div>
      <div class="content-wrapper">
        <div class="mobile-header">
          <div class="sidebar-toggle" @click="toggleSidebar"></div>
          <nuxt-link tag="h1" to="/">Open5e</nuxt-link>
          <div class="spacer"></div>
        </div>
        <ol class="breadcrumb">
          <li v-for="item in crumbs" v-bind:key="item" class="breadcrumb-item">
            <nuxt-link :to="item.path" active-class="active">
              {{ item.breadcrumb }}
            </nuxt-link>
          </li>
        </ol>
        <div class="shade" v-show="showSidebar" @click="hideSidebar"></div>
        <nuxt />
        <footer><a href="/legal/">Content provided under the OGL 1.0a</a></footer>
      </div>
    </div>
  </div>
</template>

<script>
import axios from 'axios'
import { mapGetters, mapActions } from 'vuex'

Array.prototype.groupBy = function(prop) {
  return this.reduce(function(groups, item) {
    const val = item[prop]
    groups[val] = groups[val] || []
    groups[val].push(item)
    return groups
  }, {})
}

const breadcrumbs = {
  // You should use / + name for the root route
  '/spells': 'Spells',
  // And just name of the page for child routes
  'profile-account': 'Account' 
}

export default {
  beforeCreate () {
    this.$store.dispatch('LOAD_CLASSES');
    this.$store.dispatch('LOAD_SECTIONS');
    this.$store.dispatch('LOAD_RACES');
  },
  methods: {
    doSearch: function (searchText) {
      this.$router.push({ name: 'search', query: { text: searchText }})
      this.showSidebar = false;
    },
    containsCurrentRoute: function(routes) {
      var currentRoute = this.$nuxt.$route.path;
      for(var i = 0; i < routes.length; i++) {
        if (currentRoute.search(routes[i])) {
          return true;
        }
      }
      return false;
    },
    containsAnyString: function(strings) {
      var contains = false
      if (typeof strings !== 'undefined' ) {
        for (var i = 0; i < strings.length; i++) {
          if (this.$nuxt.$route.path.indexOf(strings[i].slug) !== -1){
            contains = true;
          }
        }
        return contains;
      }
    },
    toggleSidebar: function() {
      this.showSidebar = !this.showSidebar;
    },
    hideSidebar: function() {
      this.showSidebar = false
    }
  },
  data() {
    return {
      searchText: this.$route.query.text,
      showSidebar: false,
    }
    
  },
  watch:{
    $route (to, from){
        this.showSidebar = false;
    }
  }, 
  computed: {
    ...mapActions({
      LOAD_CLASSES: 'LOAD_CLASSES',
      LOAD_SECTIONS: 'LOAD_CLASSES',
      LOAD_RACES: 'LOAD_CLASSES',
    }),
    ...mapGetters({
      classes: 'allClasses',
      sections: 'allSections',
      races: 'allRaces',
    }),
    sectionGroups: function() {
      let groupedSections = this.sections.groupBy('parent');
      return groupedSections;
    },
    charSections: function () {
      if (this.sectionGroups.hasOwnProperty('Characters')){
        let results = this.sectionGroups['Characters'].concat(this.sectionGroups['Character Advancement']);
        return results.sort(function (a,b) {
          if (a.slug < b.slug) {return -1}
          else if (a.slug > b.slug) {return 1}
          else return 0;
        })
      }
    },
    crumbs () {
      let crumbs = []
      this.$route.matched.forEach((item) => {
        if (breadcrumbs[item.name] || breadcrumbs[item.path]) {
          item.breadcrumb = breadcrumbs[item.name] || breadcrumbs[item.path]
          crumbs.push(item)
        }
      })

      return crumbs
    }
  },
}
</script>

<style lang="scss">
@import '../assets/main';

#__layout{
  overflow: hidden;
}

.shade {
  display: none;
}

.app-wrapper {
  display: flex;
  flex-direction: row;
  align-content: stretch;
  height: 100vh;
  width: 100vw;
  background: $color-fog;
  position: relative;
}

.content-wrapper {
  padding: $content-padding-y $content-padding-x;
  overflow: auto;
  flex-grow: 1;
  background: white;
  max-width: 60rem;
  .sticky-header {
    position: sticky;
    top: 0;
    z-index: 999;
  }
}

.input-search {
  position: sticky;
  top: 0;
  width: 100%;
  background: $color-blood;
  color: white;
  padding: 1rem;
  border: none;
  font-size: $font-size-base;
  outline: none;
  z-index:2;
  &::placeholder {
    color: white;
    opacity: 0.6;
  }
}

footer {
  margin-top: 1rem;
  font-size: .8rem;
  display: block;
  text-align: center;
  padding-top: 1rem;
  border-top: 1px solid $color-fog;
}

.mobile-header {
  display: none;
  width: calc(100% + 4rem);
  top: -1rem;
  height: 3rem;
  background-color: $color-fireball;
  position: sticky;
  color: white;
  flex-direction: row;
  justify-content: space-between;
  margin: (-$content-padding-y) (-$content-padding-x) 0;
  z-index: 6000;


  .sidebar-toggle {
    display: flex;
    height: 100%;
    width: 3rem;
    justify-content: center;
    align-items: center;
    background-image: url('/img/menu-button.png');
    background-size: 50%;
    background-repeat: no-repeat;
    background-position: center;

    &:hover{
      background-color: $color-blood;
      cursor: pointer;
    }
  }

  h1 {
    display: inline-block;
    margin: 0;
    padding: 0;
  }

  .spacer {
    width: 3rem;
    height: 3rem;
  }
}

.sidebar {
  color: white;
  background-color: $color-basalt;
  width: $sidebar-width;
  min-width: $sidebar-width;
  overflow-y: auto;
  font-size: 15px;
  position: relative;
  z-index: 1000;
  display: flex;
  flex-direction: column;

  .sidebar-link {
    display: inline-block;
    align-self: flex-end;
    margin-top: auto;
  }

  .sidebar-image {
    width: 100%;
    display: block;
  }

  
  h1 {
    display: block;
    background-color: $color-fireball; 
    padding: 1rem 3rem 1rem 1rem;
    cursor: pointer;
    margin-top: 0;
  }

  ul {
    padding: $pad-sm $pad-md $pad-sm $pad-xs;
    list-style: none;
    li {
      padding: $pad-md $pad-md;
      opacity: 0.8;
      cursor: pointer;

      &:hover {
        opacity: 1;
      }
      &.nuxt-link-active {
        font-weight: bold;
        opacity: 1;
      }
    }
    ul {
      background-color: $color-darkness;
      opacity: 0.8;
      padding: $pad-sm $pad-md $pad-sm $pad-lg;
      margin: 0 -1rem;
      
      li {
        padding: $pad-sm $pad-md;
      }
    }
  }
}

@media (max-width: 600px) {

  .shade {
    display: block;
    position: fixed;
    top: 0;
    left: 0;
    width: 100vw;
    height: 100vh;
    background: rgba($color-basalt, .5);
    z-index: 500;
  }
  .app-wrapper {
    position: relative;
    margin-left: -$sidebar-width;
    transition: margin-left 250ms ease;

    .mobile-header {
      display: flex;
    }

    .container {
      padding: 0;
    }

    .content-wrapper {
      min-width: 100vw;
    }
    
    .sidebar {
      min-width: $sidebar-width;
    }
  }
  .app-wrapper.show-sidebar {
    margin-left: 0;
  }
}

@media (min-width: 1200px) {
  .app-wrapper {
    .content-wrapper {
      max-width: calc(100vw - 24rem);
      overflow-x: visible;

      .side-note {
        position: absolute;
        right: 2rem;
      }
    }
  }
}

@media print {
  .app-wrapper {
    overflow-y: visible;
    height: auto;
    .content-wrapper{
      overflow-y: visible;
    }
  }
}
</style>

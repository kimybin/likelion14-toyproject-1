import { useState } from "react";

import IconHome from '../assets/icon_home.svg?react';
import IconRanking from '../assets/icon_ranking.svg?react';
import IconRelay from '../assets/icon_relay.svg?react';
import IconMypage from '../assets/icon_mypage.svg?react';

function NavBar(){
    const [activeTab, setActiveTab] = useState('home');

    const navItems = [
    { id: 'home', label: '홈', Icon: IconHome },
    { id: 'ranking', label: '완주 랭킹', Icon: IconRanking },
    { id: 'relay', label: '릴레이 인증', Icon: IconRelay },
    { id: 'mypage', label: '마이페이지', Icon: IconMypage },
    ];

    return(
      <div style={styles.navContainer}>
        {navItems.map((item) => {
          const isActive = activeTab === item.id;
          const {Icon} = item;
              
          return (
            <button
              key={item.id}
              onClick={() => setActiveTab(item.id)}
              style={{
                ...styles.navItem,
                color: isActive ? '#000000' : '#999999',
                fontWeight: 'bold',
              }}
            >
              <Icon 
                style={styles.icon} 
                fill={isActive ? '#000000' : '#999999'} 
              />
              <span style={styles.label}>{item.label}</span>
            </button>
          );
        })}
      </div>
    );
}

const styles = {
  navContainer: {
    position: 'fixed',
    bottom: 0,
    left: 0,
    right: 0,
    height: '60px',
    backgroundColor: '#ffffff',
    borderTop: '1px solid #e0e0e0',
    display: 'flex',
    justifyContent: 'space-around',
    alignItems: 'center',
    paddingBottom: 'env(safe-area-inset-bottom)',
    zIndex: 1000,
  },
  navItem: {
    background: 'none',
    border: 'none',
    display: 'flex',
    flexDirection: 'column',
    alignItems: 'center',
    cursor: 'pointer',
    width: '25%',
  },
  icon: {
    width: '24px',
    height: '24px',
    marginBottom: '4px',
    transition: 'fill 0.2s ease',
  },
  label: {
    fontSize: '11px',
  },
};

export default NavBar;
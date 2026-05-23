import BottomNav from './components/NavBar';

function App() {
  return (
    <div style={{ paddingBottom: '60px' }}>
      {/* 실제 콘텐츠가 들어갈 자리 */}
      <div style={{ padding: '20px', textAlign: 'center' }}>
        <h2>swsy팀 프로젝트</h2>
        <p>하단 탭 바를 눌러보세요.</p>
      </div>

      {/* 하단 탭 바 부품 삽입 */}
      <BottomNav />
    </div>
  );
}

export default App;
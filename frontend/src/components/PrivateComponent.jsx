const PrivateComponent = () => {
    const { isLoggedIn, username } = useAuth();
    const navigate = useNavigate();
    const [loading, setLoading] = useState(true);
  
    useEffect(() => {
      setLoading(false);
      if (!isLoggedIn) {
        navigate("/login");
      }
    }, [isLoggedIn, navigate]);
  
    if (loading) return <p>Loading...</p>;
    return isLoggedIn ? <h2>Welcome {username}! This is the private section.</h2> : null;
  };
  
import PropTypes from 'prop-types';

export default function Wrapper({ children }) {
  return (
    <div id="wrapper" style={{ margin: '40px' }}>
      {children}
    </div>
  );
}

Wrapper.propTypes = {
  children: PropTypes.node.isRequired,
};
